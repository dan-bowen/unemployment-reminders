import json
import pytz
from datetime import datetime, timezone, time
from lib.twilio import TwilioClient, TwilioClientException
from lib.collect import CollectNextAlert
from api.repo import AlertsRepo

alerts_repo = AlertsRepo()
message_footer = "Thanks for using my app.\nhttps://www.crucialwebstudio.com"


class TwilioBot:
    # TODO actually ask the user for these
    default_timezone = 'America/Chicago'
    default_alert_time = '09:30:00'

    def __init__(self, app=None):
        self.app = app

        self.base_url = None
        self.sms_number = None
        self.twilio_client = None
        self.collected_next_alert = None
        self.collected_phone_number = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.base_url = app.config['BOT_BASE_URL']
        self.sms_number = app.config['BOT_SMS_NUMBER']
        self.twilio_client = TwilioClient(
            app.config['SECRETS'].TWILIO_ACCOUNT_SID,
            app.config['SECRETS'].TWILIO_AUTH_TOKEN
        )

    def ask_next_alert(self):
        return {
            "actions": [
                {
                    "collect": {
                        "name":        "next_certification_date",
                        "questions":   [
                            {
                                "question": "What is your next certification day?",
                                "name":     "next_certification_date",
                                "validate": {
                                    "on_failure":   {
                                        "messages": [
                                            {
                                                "say": (
                                                    f"I'm sorry, that isn't a day I recognize. "
                                                    f"You can say things like Monday, Next Monday, etc."
                                                )
                                            }
                                        ]
                                    },
                                    "webhook":      {
                                        "method": "POST",
                                        "url":    f"{self.base_url}/bot/validate-certification-date"
                                    },
                                    "max_attempts": {
                                        "redirect":     "task://collect_fallback",
                                        "num_attempts": 3
                                    }
                                }
                            }
                        ],
                        "on_complete": {
                            "redirect": f"{self.base_url}/bot/say-thanks"
                        }
                    }
                }
            ]
        }

    def collect_next_alert(self, form_post):
        """Collects certification date from Twilio POST"""
        memory = json.loads(form_post.get('Memory'))
        answers = memory['twilio']['collected_data']['next_certification_date']['answers']

        self.collected_next_alert = answers['next_certification_date']['answer']

    def validate_next_alert(self, form_post):
        is_valid = CollectNextAlert(form_post['CurrentInput']).is_valid
        return {'valid': is_valid}

    def collect_phone_number(self, phone_number):
        self.collected_phone_number = phone_number

    def create_alert_model(self):
        now = datetime.now(timezone.utc)
        next_alert = CollectNextAlert(self.collected_next_alert,
                                      timezone=self.default_timezone,
                                      alert_time=self.default_alert_time)

        alert_model = dict(phone_number=self.collected_phone_number,
                           timezone=self.default_timezone,
                           alert_time=self.default_alert_time,
                           next_alert_at=next_alert.next_alert_at(now).isoformat(),
                           in_progress=0,
                           certification_day=next_alert.day_of_week
                           )

        return alert_model

    def subscribe(self):
        alerts_repo.create_alert(self.create_alert_model())

    def say_thanks(self):
        alert_model = self.create_alert_model()
        next_alert = datetime.fromisoformat(alert_model['next_alert_at'])
        default_timezone = pytz.timezone(self.default_timezone)
        formatted_date = next_alert.astimezone(default_timezone).strftime('%A, %B %d at %I:%M %p')
        return {
            'actions': [
                {
                    'say': (
                        f"Okay great. I'll remind you on {formatted_date} and every two weeks after that.\n\n"
                        f"{message_footer}"
                    )
                }
            ]
        }

    def unsubscribe(self, form_post):
        phone_number = form_post['UserIdentifier']
        alerts_repo.delete_alert(phone_number)

    def say_goodbye(self):
        return {
            'actions': [
                {
                    'say': (
                        f"Thanks for letting me know. I'll stop sending reminders."
                        f"{message_footer}"
                    )
                }
            ]
        }

    def say_reminder(self, phone_number):
        try:
            message = self.twilio_client.send_sms(
                to=phone_number,
                from_=self.sms_number,
                body=(
                    f"This is a friendly reminder. Don't forget to certify for unemployment benefits today. "
                    f"Good luck with your job search.\n\n"
                    f"{message_footer}"
                )
            )
        except TwilioClientException:
            raise TwilioBotException(f'Failed to send reminder for phone number: {phone_number}')

        return message


class TwilioBotException(Exception):
    pass

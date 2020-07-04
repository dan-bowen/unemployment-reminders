import json
import pytz
from datetime import datetime, time
from config import config
from lib.twilio import TwilioClient, TwilioClientException
from .collect import CollectNextAlert
from .repo import alerts

twilio_client = TwilioClient(
    config.SECRETS.TWILIO_ACCOUNT_SID,
    config.SECRETS.TWILIO_AUTH_TOKEN
)
message_footer = "Thanks for using my app.\nhttps://www.crucialwebstudio.com"


class ReminderBot:
    # TODO actually ask the user for these
    default_timezone = 'America/Chicago'
    default_alert_time = '09:30:00'

    def __init__(self):
        self.base_url = config.BOT_BASE_URL
        self.sms_number = config.BOT_SMS_NUMBER
        self.inbound_message = None

    def receive_message(self, form_post):
        """Receive message from Twilio-Autopilot"""

        # form_post is an ImmutableDict so we assemble our own return dict
        self.inbound_message = {
            'CurrentTask':           form_post.get('CurrentTask'),
            'CurrentInput':          form_post.get('CurrentInput'),
            'Channel':               form_post.get('Channel'),
            'NextBestTask':          form_post.get('NextBestTask'),
            'CurrentTaskConfidence': form_post.get('CurrentTaskConfidence'),
            'AssistantSid':          form_post.get('AssistantSid'),
            'AccountSid':            form_post.get('AccountSid'),
            'UserIdentifier':        form_post.get('UserIdentifier'),
            'DialoguePayloadUrl':    form_post.get('DialoguePayloadUrl'),
            # Memory is a JSON string so we extract it here
            'Memory':                json.loads(form_post.get('Memory'))
        }

    def say_intro(self, phone_number):
        try:
            message = twilio_client.send_sms(
                to=phone_number,
                from_=self.sms_number,
                body=(
                    f"Welcome to the Unemployment Reminders chatbot. Here are a few commands you can use.\n\n"
                    f"REMIND ME to set or change a reminder.\n\n"
                    f"FOUND A JOB to cancel the remidner."
                )
            )
        except TwilioClientException:
            raise ReminderBotException(f'Failed to send intro for phone number: {phone_number}')

        return message

    def ask_next_alert(self):
        return {
            "actions": [
                {
                    "collect": {
                        "name":        "next_alert_date",
                        "questions":   [
                            {
                                "question": (
                                    "What is your next certification day?\n\n"
                                    "You can say things like Monday, Next Monday, etc."
                                ),
                                "name":     "next_alert_date",
                                "validate": {
                                    "on_failure":   {
                                        "messages": [
                                            {
                                                "say": (
                                                    "I'm sorry, that isn't a day I recognize. Please try again.\n\n"
                                                    "You can say things like Monday, Next Monday, etc."
                                                )
                                            }
                                        ]
                                    },
                                    "webhook":      {
                                        "method": "POST",
                                        "url":    f"{self.base_url}/bot/validate-next-alert"
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

    def validate_next_alert(self):
        is_valid = CollectNextAlert(self.inbound_message['CurrentInput']).is_valid
        return {'valid': is_valid}

    def create_alert_model(self):
        answers = self.inbound_message['Memory']['twilio']['collected_data']['next_alert_date']['answers']
        next_alert = CollectNextAlert(answers['next_alert_date']['answer'],
                                      timezone=self.default_timezone,
                                      alert_time=self.default_alert_time)

        alert_model = dict(phone_number=self.inbound_message['UserIdentifier'],
                           timezone=self.default_timezone,
                           alert_time=self.default_alert_time,
                           next_alert_at=next_alert.next_alert_at().isoformat(),
                           in_progress=0,
                           alert_day=next_alert.day_of_week
                           )

        return alert_model

    def subscribe(self):
        alerts.create_alert(self.create_alert_model())

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
                        f"Found a job?\n\n"
                        f"Reply FOUND A JOB to cancel the reminder.\n\n"
                        f"{message_footer}"
                    )
                }
            ]
        }

    def unsubscribe(self):
        alerts.delete_alert(self.inbound_message['UserIdentifier'])

    def say_goodbye(self):
        return {
            'actions': [
                {
                    'say': (
                        f"You have been unsubscribed from all messages.\n\n"
                        f"Reply START, or UNTSOP to restart messages.\n\n"
                        f"{message_footer}"
                    )
                }
            ]
        }

    def say_congrats(self):
        return {
            'actions': [
                {
                    'say': (
                        f"Congrats on finding a new job!\n\n"
                        f"The reminder has been cancelled.\n\n"
                        f"{message_footer}"
                    )
                }
            ]
        }

    def say_fallback(self):
        return {
            "actions": [
                {
                    "say": "I'm sorry didn't quite get that. Please say that again."
                },
                {
                    "listen": True
                }
            ]
        }

    def say_reminder(self, phone_number):
        try:
            message = twilio_client.send_sms(
                to=phone_number,
                from_=self.sms_number,
                body=(
                    f"Today is certification day. Be sure to file your certification to retain your benefits.\n\n"
                    f"Best of luck with your job search.\n\n"
                    f"Found a job?\n\n"
                    f"Reply FOUND A JOB and we'll cancel the reminder.\n\n"
                    f"{message_footer}"
                )
            )
        except TwilioClientException:
            raise ReminderBotException(f'Failed to send reminder for phone number: {phone_number}')

        return message


class ReminderBotException(Exception):
    pass

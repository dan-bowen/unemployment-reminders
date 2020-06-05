import json
from datetime import datetime, timezone, time
from lib.collect import CollectNextAlert
from api.repo import AlertsRepo


class TwilioBot:
    def __init__(self, app=None):
        self.app = app
        self.alerts_repo = AlertsRepo()

        self.base_url = None
        self.collected_next_alert = None
        self.collected_timezone = None
        self.collected_alert_time = None
        self.collected_phone_number = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.base_url = app.config['BOT_BASE_URL']

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
                                                "say": "That isn't a day I recognize. You can say things like Monday, Next Monday, etc."
                                            }
                                        ]
                                    },
                                    "webhook":      {
                                        "method": "POST",
                                        "url":    f"{self.base_url}/bot/validate-certification-date"
                                    },
                                    "max_attempts": {
                                        "redirect":     "task://having_trouble",
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

    def collect_timezone(self, timezone):
        """Ex: America/Chicago"""
        self.collected_timezone = timezone

    def collect_alert_time(self, alert_time):
        """ISO 8601 formatted time part"""
        self.collected_alert_time = alert_time

    def collect_phone_number(self, phone_number):
        self.collected_phone_number = phone_number

    def create_alert_model(self):
        now = datetime.now(timezone.utc)
        next_alert = CollectNextAlert(self.collected_next_alert,
                                      timezone=self.collected_timezone,
                                      alert_time=self.collected_alert_time)

        alert_model = dict(phone_number=self.collected_phone_number,
                           timezone=self.collected_timezone,
                           alert_time=self.collected_alert_time,
                           next_alert_at=next_alert.next_alert_at(now).isoformat(),
                           in_progress=0,
                           certification_day=next_alert.day_of_week
                           )

        return alert_model

    def subscribe(self):
        self.alerts_repo.create_alert(self.create_alert_model())

    def say_thanks(self):
        message = (
            f'Okay great. I\'ll remind you on {self.collected_next_alert} and every two weeks after that.'
            f' Thanks for using my app.'
        )
        return {
            'actions': [
                {'say': message}
            ]
        }

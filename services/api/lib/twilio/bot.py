import json
from lib.collect import CollectNextAlert
from api.repo import AlertsRepo


class TwilioBot:
    def __init__(self, app=None):
        self.app = app
        self.alerts_repo = AlertsRepo()

        self.base_url = None
        self.collected_next_alert = None

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

    def subscribe(self, alert_model):
        self.alerts_repo.create_alert(alert_model)

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

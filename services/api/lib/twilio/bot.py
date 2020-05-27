import json


class TwilioBot:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.collected_certification_date = None

    def ask_certification_date(self):
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

    def collect_certification_date(self, params):
        memory = json.loads(params.get('Memory'))
        answers = memory['twilio']['collected_data']['next_certification_date']['answers']
        next_certification_date = answers['next_certification_date']['answer']

        self.collected_certification_date = next_certification_date

    def say_thanks(self):
        message = (
            f'Okay great. I\'ll remind you on {self.collected_certification_date} and every two weeks after that.'
            f' Thanks for using my app.'
        )
        return {
            'actions': [
                {'say': message}
            ]
        }

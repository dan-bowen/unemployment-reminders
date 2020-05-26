import json


class TwilioBot:
    def __init__(self):
        self.collected_certification_date = None

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

import unittest
import json
import helpers
from lib.twilio import TwilioBot


class BotCollectorTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()
        self.bot = TwilioBot(base_url=self.helper.app.config['BOT_BASE_URL'])

    def tearDown(self):
        pass

    def test_validate_certification_date(self):
        # valid response
        path = '/bot/validate-certification-date'
        params = {'CurrentInput': 'next monday'}
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'valid': True})

        # invalid response
        path = '/bot/validate-certification-date'
        params = {'CurrentInput': 'this is not a valid response'}
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'valid': False})

    def test_ask_certification_date(self):
        response = self.helper.twilio_request('POST', '/bot/ask-certification-date', {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.bot.ask_certification_date())

    def test_say_thanks(self):
        path = '/bot/say-thanks'
        params = {
            'Memory': json.dumps({
                'twilio': {
                    'collected_data': {
                        'next_certification_date': {
                            'answers': {
                                'next_certification_date': {
                                    'answer': 'next monday'
                                }
                            }
                        }
                    }
                }
            })
        }

        self.bot.collect_certification_date(params)

        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.bot.say_thanks())


if __name__ == "__main__":
    unittest.main()

import unittest
import json
import helpers
from lib.twilio import TwilioBot


class TwilioCollectorTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()

    def tearDown(self):
        pass

    def test_valid_certification_date(self):
        path = '/twilio/validate-certification-date'
        params = {'CurrentInput': 'next monday'}
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'valid': True})

    def test_invalid_certification_date(self):
        path = '/twilio/validate-certification-date'
        params = {'CurrentInput': 'this is not a valid response'}
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'valid': False})

    def test_finalize_collector(self):
        path = '/twilio/collect'
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

        twilio_bot = TwilioBot()
        twilio_bot.collect_certification_date(params)

        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, twilio_bot.say_thanks())


if __name__ == "__main__":
    unittest.main()

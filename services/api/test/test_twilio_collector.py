import unittest
import helpers


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


if __name__ == "__main__":
    unittest.main()

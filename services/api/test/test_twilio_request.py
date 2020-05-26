import unittest
import helpers


class TwilioTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()

    def tearDown(self):
        pass

    def test_allow_twilio_request(self):
        path = '/twilio/ping'
        params = {}
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)

    def test_deny_twilio_request(self):
        path = '/twilio/ping'
        params = {}
        response = self.helper.twilio_request('POST', path, params, valid=False)
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()

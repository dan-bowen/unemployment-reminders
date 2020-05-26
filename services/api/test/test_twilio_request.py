import unittest
import helpers


class TwilioTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()

    def tearDown(self):
        pass

    def test_validate_twilio_request(self):
        path = '/bot/ping'
        params = {}

        # valid request
        response = self.helper.twilio_request('POST', path, params)
        self.assertEqual(response.status_code, 200)

        # invalid request
        response = self.helper.twilio_request('POST', path, params, valid=False)
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()

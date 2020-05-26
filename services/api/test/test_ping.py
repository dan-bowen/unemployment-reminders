import unittest
import helpers


class RegisterTests(unittest.TestCase):

    def setUp(self):
        helper = helpers.Helper()
        self.client = helper.client

    def tearDown(self):
        pass

    def test_ping(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'db_access_result': 'exception',
            'external_http_result': 'success'
        })


if __name__ == "__main__":
    unittest.main()

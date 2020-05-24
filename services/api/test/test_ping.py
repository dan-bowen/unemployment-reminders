import unittest
import helpers


class RegisterTests(unittest.TestCase):

    def setUp(self):
        helper = helpers.Helper()
        helper.clean_db()

        self.client = helper.client

    def tearDown(self):
        pass

    def test_ping(self):
        response = self.client.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
              "data": {
                "attributes": {
                  "result": "success"
                },
                "id": None,
                "links": {
                  "self": "/ping"
                },
                "type": "Ping"
              },
              "links": {
                "self": "/ping"
              }
            }
        )


if __name__ == "__main__":
    unittest.main()

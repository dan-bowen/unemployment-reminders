import unittest
import helpers
from lib.twilio import TwilioBot


class BotTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()
        self.bot = TwilioBot(base_url=self.helper.app.config['BOT_BASE_URL'])

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()

import json
import unittest
import helpers
from lib.twilio import TwilioBot


class BotTests(unittest.TestCase):

    def setUp(self):
        self.helper = helpers.Helper()
        self.bot = TwilioBot(app=self.helper.app)

    def tearDown(self):
        pass

    # def test_create_alert_model(self):
    #     form_post = {
    #         'Memory': json.dumps({'twilio': {
    #             'collected_data': {
    #                 'next_certification_date': {
    #                     'answers': {
    #                         'next_certification_date': {
    #                             'answer': 'next monday'
    #                         }
    #                     }
    #                 }
    #             }
    #         }})
    #     }
    #     self.bot.collect_next_alert(form_post)
    #
    #     self.bot.collect_timezone('America/Chicago')
    #     self.bot.collect_alert_time('09:30:00')
    #     self.bot.collect_phone_number('7735551234')
    #
    #     expected = {
    #         'phone_number': '7735551234',
    #         'alert_time': '09:30:00',
    #         'timezone': 'America/Chicago',
    #         'in_progress': 0,
    #         'certification_day': 'monday',
    #         'next_alert_at': ''
    #     }
    #     actual = self.bot.create_alert_model()
    #     self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

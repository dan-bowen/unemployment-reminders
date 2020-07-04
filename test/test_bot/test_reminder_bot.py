import json
from datetime import datetime
from unittest import TestCase, mock
from bot import ReminderBot


class BotTests(TestCase):

    def setUp(self):
        self.bot = ReminderBot()

    def tearDown(self):
        pass

    @mock.patch('bot.reminder_bot.get_utc_now', return_value=datetime.fromisoformat('2020-06-01T10:00:00+00:00'))
    def test_create_alert_model(self, mock_utc_now):
        """Generate the alert model to insert into data store"""
        form_post = {
            'CurrentTask': 'remind_me',
            'CurrentInput': 'Remind me ',
            'Channel': 'sms',
            'NextBestTask': '',
            'CurrentTaskConfidence': '1.0',
            'AssistantSid': '{SOME_GUID}',
            'AccountSid': '{SOME_GUID}',
            'UserIdentifier': '+17735551234',
            'DialoguePayloadUrl': 'https://autopilot.twilio.com/v1/Assistants/{GUID_1}/Dialogues/{GUID_2}',
            'Memory': json.dumps({'twilio': {
                'sms': {
                    'To': '+17735554321',
                    'From': '+17735551234',
                    'MessageSid': '{SOME_GUID}'
                },
                'collected_data': {
                    'next_alert_date': {
                        'answers': {
                            'next_alert_date': {
                                'answer': 'next monday'
                            }
                        }
                    }
                }
            }})
        }
        self.bot.receive_message(form_post)

        expected = {
            'phone_number': '+17735551234',
            'timezone': 'America/Chicago',
            'alert_day': 'monday',
            'alert_time': '09:30:00',
            'in_progress': 0,
            'next_alert_at': '2020-06-15T14:30:00+00:00'
        }
        actual = self.bot.create_alert_model()
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

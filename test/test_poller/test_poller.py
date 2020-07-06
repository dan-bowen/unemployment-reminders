from unittest import TestCase, mock
import poller

cloudwatch_event = {
    "version":     "0",
    "id":          "53dc4d37-cffa-4f76-80c9-8b7d4a4d2eaa",
    "detail-type": "Scheduled Event",
    "source":      "aws.events",
    "account":     "123456789012",
    "time":        "2015-10-08T16:53:06Z",
    "region":      "us-east-1",
    "resources":   [
        "arn:aws:events:us-east-1:123456789012:rule/my-scheduled-rule"
    ],
    "detail":      {}
}


class PollerTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('poller.alerts_repo')
    @mock.patch('poller.bot')
    def test_handler(self, mock_bot, mock_alerts_repo):
        pending_alerts = [
            {
                'phone_number': '+17735551234',
                'next_alert_at': '2020-06-01T10:00:00+00:00',
                'alert_day': 'monday',
                'timezone': 'America/Chicago',
                'alert_time': '09:30'
            }
        ]

        mock_alerts_repo.get_pending_alerts.return_value = pending_alerts

        expected = pending_alerts
        actual = poller.lambda_handler(cloudwatch_event, None)

        # assert expected return value of the function
        self.assertEqual(expected, actual)

        # assert pending alerts are pulled from DB
        mock_alerts_repo.get_pending_alerts.assert_called_once()

        # assert that in_progress flag was set on each pending alert
        mock_alerts_repo.set_in_progress.assert_has_calls(
            [mock.call(alert['phone_number']) for alert in pending_alerts]
        )

        # assert that an alert was attempted on each pending alert
        mock_bot.say_reminder.assert_has_calls(
            [mock.call(alert['phone_number']) for alert in pending_alerts]
        )

        # assert that the next alert date was applied to each pending alert
        self.assertEqual(len(pending_alerts), mock_alerts_repo.set_next_alert.call_count)

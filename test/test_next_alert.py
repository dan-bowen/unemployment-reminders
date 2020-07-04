from unittest import TestCase, mock
from datetime import datetime
from bot.collect import CollectNextAlert, CollectException


class NextAlertTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        # valid
        for response in ('monday', 'MonDaY', 'next monday', 'Next MonDay'):
            self.assertTrue(CollectNextAlert(response).is_valid)

        # invalid
        for response in ('moday', 'this is wrong'):
            cert_date = CollectNextAlert(response)
            self.assertFalse(cert_date.is_valid)

            # throw exception when accessing properties on invalid collector
            with self.assertRaises(CollectException):
                sequence = cert_date.sequence

            with self.assertRaises(CollectException):
                dow = cert_date.day_of_week

    def test_get_sequence(self):
        self.assertEqual(CollectNextAlert('monday').sequence, 0)
        self.assertEqual(CollectNextAlert('next monday').sequence, 1)

    def test_day_of_week(self):
        for day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'MoNdaY', 'TueSdaY', 'WednEsdaY', 'ThurSdaY', 'FriDaY'):
            self.assertEqual(CollectNextAlert(day).day_of_week, day.lower())

    @mock.patch('bot.collect.next_alert.get_utc_now')
    def test_next_alert_this_weekday(self, mock_utc_now):
        cert_date = CollectNextAlert('monday', timezone='America/Chicago', alert_time='10:30:00')

        # monday, June 1
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-01T10:00:00-05:00')
        actual = cert_date.next_alert_at()
        # monday, June 8
        expected = datetime.fromisoformat('2020-06-08T15:30:00+00:00')
        self.assertEqual(actual, expected)

        # tuesday, June 2
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-02T10:00:00-05:00')
        actual = cert_date.next_alert_at()
        # monday, June 8
        expected = datetime.fromisoformat('2020-06-08T15:30:00+00:00')
        self.assertEqual(actual, expected)

        # monday, June 8
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-08T10:00:00-05:00')
        actual = cert_date.next_alert_at()
        # monday, June 15
        expected = datetime.fromisoformat('2020-06-15T15:30:00+00:00')
        self.assertEqual(actual, expected)

    @mock.patch('bot.collect.next_alert.get_utc_now')
    def test_next_alert_next_weekday(self, mock_utc_now):
        cert_date = CollectNextAlert('next monday', timezone='America/Chicago', alert_time='10:30:00')

        # monday, June 1
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-01T10:00:00-05:00')
        # print(local_now.isoformat())
        actual = cert_date.next_alert_at()
        # monday, June 15
        expected = datetime.fromisoformat('2020-06-15T15:30:00+00:00')
        # print(expected.isoformat())
        self.assertEqual(actual, expected)

        # tuesday, June 2
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-02T10:00:00-05:00')
        actual = cert_date.next_alert_at()
        # monday, June 15
        expected = datetime.fromisoformat('2020-06-15T15:30:00+00:00')
        self.assertEqual(actual, expected)

        # monday, June 8
        mock_utc_now.return_value = datetime.fromisoformat('2020-06-08T10:00:00-05:00')
        actual = cert_date.next_alert_at()
        # monday, June 22
        expected = datetime.fromisoformat('2020-06-22T15:30:00+00:00')
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

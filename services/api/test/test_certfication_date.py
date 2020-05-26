import unittest
from lib.collect import CollectCertificationDate, CollectException


class CertificationDateTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_input(self):
        # valid
        for response in ('monday', 'MonDaY', 'next monday', 'Next MonDay'):
            self.assertTrue(CollectCertificationDate(response).is_valid)

        # invalid
        for response in ('moday', 'this is wrong'):
            self.assertFalse(CollectCertificationDate(response).is_valid)

            # throw exception when accessing properties on invalid collector
            with self.assertRaises(CollectException):
                CollectCertificationDate(response).sequence

            with self.assertRaises(CollectException):
                CollectCertificationDate(response).day_of_week

    def test_get_sequence(self):
        self.assertEqual(CollectCertificationDate('monday').sequence, 0)
        self.assertEqual(CollectCertificationDate('next monday').sequence, 1)

    def test_day_of_week(self):
        for day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'MoNdaY', 'TueSdaY', 'WednEsdaY', 'ThurSdaY', 'FriDaY'):
            self.assertEqual(CollectCertificationDate(day).day_of_week, day.lower())


if __name__ == "__main__":
    unittest.main()

from unittest import TestCase

from model.period import create_period


class TestPeriod(TestCase):

    def test_create_period(self):
        expected_period = {
            'start': None,
            'stop': None
        }
        created_period = create_period()

        self.assertEqual(created_period, expected_period)

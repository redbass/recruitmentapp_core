from datetime import datetime

from freezegun import freeze_time

from model.period import create_period
from test import UnitTestCase


class TestPeriod(UnitTestCase):

    def test_create_period(self):
        start_date = datetime(1985, 10, 26)
        end_date = datetime(2015, 10, 21)
        created_period = create_period(start=start_date, end=end_date)

        self.assertEqual(created_period['start'], start_date)
        self.assertEqual(created_period['end'], end_date)

    def test_create_period_no_start(self):
        start_date = datetime(1985, 10, 26)
        end_date = datetime(2015, 10, 21)

        with freeze_time(start_date):
            created_period = create_period(start=None, end=end_date)

            self.assertEqual(created_period['start'], start_date)
            self.assertEqual(created_period['end'], end_date)

    def test_create_period_no_end(self):
        start_date = datetime(1985, 10, 26)
        end_date = datetime(2015, 10, 21)

        with freeze_time(start_date):
            created_period = create_period(start=None, end=end_date)

            self.assertEqual(created_period['start'], start_date)
            self.assertEqual(created_period['end'], end_date)

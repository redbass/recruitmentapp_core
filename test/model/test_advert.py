from datetime import datetime, timedelta
from freezegun import freeze_time

from db.collections import jobs
from model.advert import create_advert, AdvertStatus
from model.period import create_period
from test import UnitTestCase


class BaseTestAdvert(UnitTestCase):

    def tearDown(self):
        super().tearDown()
        jobs.drop()


class TestAdvertStatus(UnitTestCase):

    def test_advert_status_equality(self):
        self.assertEqual(AdvertStatus.DRAFT, AdvertStatus.DRAFT)
        self.assertEqual(AdvertStatus.DRAFT, "DRAFT")

        self.assertNotEqual(AdvertStatus.DRAFT, AdvertStatus.APPROVED)
        self.assertNotEqual(AdvertStatus.DRAFT, "something")


class TestCreateAdvert(BaseTestAdvert):
    freeze_date = datetime(year=1985, month=10, day=26)

    @freeze_time(freeze_date)
    def test_create_advert(self):
        period = create_period(start=datetime.now() + timedelta(days=3),
                               end=datetime.now() + timedelta(days=33))

        expected_advert = {
            'status': AdvertStatus.DRAFT,
            'deleted': False,
            'period': period,
            'date': {
                'created': datetime.utcnow(),
                'expire': None
            }
        }

        advert = create_advert(period=period)
        self.assertIsNotNone(advert.pop('_id'))
        self.assertEqual(expected_advert, advert)

    def test_create_advert_with_wrong_period(self):
        with self.assertRaises(ValueError):
            create_advert(period=None)

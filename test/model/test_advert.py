from datetime import datetime

from freezegun import freeze_time

from db.collections import jobs
from model.advert import create_advert, AdvertStatus
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
        duration = 30
        advert = create_advert(duration=duration)
        expected_advert = {
            '_id': advert['_id'],
            'status': AdvertStatus.DRAFT,
            'duration': duration,
            'date': {
                'created': datetime.utcnow(),
                'updated': datetime.utcnow()
            }
        }
        self.assertEqual(expected_advert, advert)

    def test_create_advert_with_wrong_period(self):
        self._assert_invalid_duration(0)
        self._assert_invalid_duration(-1)

    def _assert_invalid_duration(self, duration):
        with self.assertRaisesRegex(
                ValueError,
                '{d} is not a valid duration period'.format(d=duration)):
            create_advert(duration=duration)

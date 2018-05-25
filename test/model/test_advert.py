from datetime import datetime
from freezegun import freeze_time

from db.collections import jobs
from model.advert import create_advert, AdvertStatus
from model.job import get_job, create_job
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
        job = create_job(title="Title", description="Description")
        job_id = job['_id']

        expected_advert = create_advert(job_id=job_id)

        job = get_job(job_id=job_id)

        self.assertTrue(job.get('adverts'))
        advert = job['adverts'][0]
        self.assertEqual(expected_advert, advert)
        self.assertEqual(AdvertStatus.DRAFT, advert['status'])
        self.assertFalse(advert['deleted'])
        self.assertEqual(advert['date']['created'], self.freeze_date)
        self.assertIsNone(advert['date']['expire'])

    def test_create_advert_wrong_job_id(self):
        with self.assertRaises(AttributeError):
            create_advert(job_id="")

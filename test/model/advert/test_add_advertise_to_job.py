from model.advert import AdvertStatus
from datetime import datetime

from freezegun import freeze_time

from db.collections import jobs
from model.job.job_advert import create_advert_for_a_job
from test.model.job import BaseTestJob, JobFactory


class TestAddAdvertToJob(BaseTestJob):

    frozen_date = datetime(year=2015, month=10, day=26)

    def test_create_advert_for_a_job(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        expected_duration = 10

        with freeze_time(self.frozen_date):
            create_advert_for_a_job(job_id=job_id,
                                    advert_duration=expected_duration)
        job = jobs.find_one({'_id': job_id})
        advert = job['adverts'][0]

        self.assertEqual(AdvertStatus.DRAFT, advert['status'])
        self.assertEqual(expected_duration, advert['duration'])
        self.assertEqual(self.frozen_date, advert['date']['created'])

    def test_create_advert_for_a_job_with_invalid_id(self):
        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id=None, advert_duration=1)

        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id="", advert_duration=1)

        result = jobs.find({}).count()
        self.assertEqual(0, result)

    def test_create_advert_for_a_job_not_in_db(self):

        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id="1", advert_duration=1)

        result = jobs.find({}).count()
        self.assertEqual(0, result)

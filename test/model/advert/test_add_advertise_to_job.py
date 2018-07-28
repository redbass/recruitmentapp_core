from model.advert import AdvertStatus
from datetime import datetime

from freezegun import freeze_time

from db.collections import jobs
from model.job.create_job import create_job
from model.job.job_advert import create_advert_for_a_job
from test.model.job import BaseTestJob


class TestAddAdvertToJob(BaseTestJob):

    frozen_date = datetime(year=2015, month=10, day=26)

    def test_create_advert_for_a_job(self):
        job = create_job(company_id=self.company['_id'],
                         title="Some title",
                         description="Some description")
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

    def test_job_date_updated(self):
        with freeze_time(self.frozen_date):
            expected_creation_date = datetime.now()
            create_job(company_id=self.company['_id'],
                       title="title",
                       description="description")
            job = jobs.find_one({})
            date = job.get('date')
            self.assertEqual(date.get('created'), expected_creation_date)
            self.assertEqual(date.get('updated'), expected_creation_date)

        with freeze_time("2015-10-27"):
            expected_modification_date = datetime.now()
            create_advert_for_a_job(job_id=job.get('_id'), advert_duration=1)
            job = jobs.find_one({})
            date = job.get('date')
            self.assertEqual(date.get('created'), expected_creation_date)
            self.assertEqual(date.get('updated'), expected_modification_date)

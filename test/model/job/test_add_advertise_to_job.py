from datetime import datetime, timedelta

from freezegun import freeze_time

from db.collections import jobs
from model.advert import create_advert
from model.job import create_job, create_advert_for_a_job
from model.period import create_period
from test.model.job import BaseTestJob


class TestAddAdvertToJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_create_advert_for_a_job(self):
        title = "Some title"
        description = "Some description"
        job = create_job(title=title, description=description)

        start_period = datetime.now()
        end_period = datetime.now() + timedelta(days=30)
        period1 = create_period(start=start_period, end=end_period)
        period2 = create_period(start=start_period, end=end_period)
        job_id = job['_id']

        create_advert_for_a_job(job_id=job_id, start_period=start_period,
                                end_period=end_period)
        create_advert_for_a_job(job_id=job_id, start_period=start_period,
                                end_period=end_period)

        result = jobs.find_one({'_id': job_id})

        expected_adverts = [create_advert(period1), create_advert(period2)]

        self.assertEqual(result['_id'], job_id)

        for advert, expected in zip(result['adverts'], expected_adverts):
            advert.pop('_id')
            expected.pop('_id')
            self.assertEqual(advert, expected)

    def test_create_advert_for_a_job_with_invalid_id(self):
        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id=None, start_period=datetime.now(),
                                    end_period=datetime.now())

        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id="", start_period=datetime.now(),
                                    end_period=datetime.now())

        result = jobs.find({}).count()
        self.assertEqual(0, result)

    def test_create_advert_for_a_job_not_in_db(self):

        with self.assertRaises(ValueError):
            create_advert_for_a_job(job_id="1", start_period=datetime.now(),
                                    end_period=datetime.now())

        result = jobs.find({}).count()
        self.assertEqual(0, result)

    def test_job_date_updated(self):
        with freeze_time("2015-10-26"):
            expected_creation_date = datetime.now()
            create_job(title="title", description="description")
            job = jobs.find_one({})
            date = job.get('date')
            self.assertEqual(date.get('created'), expected_creation_date)
            self.assertEqual(date.get('updated'), expected_creation_date)

        with freeze_time("2015-10-27"):
            expected_modification_date = datetime.now()
            create_advert_for_a_job(
                job_id=job.get('_id'),
                start_period=datetime.now(),
                end_period=datetime.now() + timedelta(days=30))
            job = jobs.find_one({})
            date = job.get('date')
            self.assertEqual(date.get('created'), expected_creation_date)
            self.assertEqual(date.get('updated'), expected_modification_date)

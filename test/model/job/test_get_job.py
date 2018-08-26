from freezegun import freeze_time

from model.job.job import get_job, get_jobs
from test.model.company import CompanyFactory
from test.model.job import BaseTestJob, JobFactory


class TestGetJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_get_job(self):
        expected_job = self.create_from_factory(JobFactory)
        job_id = expected_job['_id']

        job = get_job(job_id)

        self.assertEqual(expected_job, job)

    def test_get_job_invalid_id(self):
        self.create_from_factory(JobFactory)

        with self.assertRaises(ValueError):
            get_job(None)

        with self.assertRaises(ValueError):
            get_job("")

        with self.assertRaises(ValueError):
            get_job("valid id")

    @freeze_time("2015-10-26")
    def test_get_jobs(self):
        company = self.create_from_factory(CompanyFactory)
        expected_job_1 = self.create_from_factory(JobFactory, title="Title 1",
                                                  company_id=company['_id'])
        expected_job_2 = self.create_from_factory(JobFactory, title="Title 2",
                                                  company_id=company['_id'])

        jobs = list(get_jobs())

        self.assertEqual(
            [expected_job_1['_id'], expected_job_2['_id']],
            [j['_id'] for j in jobs])

        self.assertEqual(
            [company['name'], company['name']],
            [j['company_name'] for j in jobs])

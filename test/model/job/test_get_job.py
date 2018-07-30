from freezegun import freeze_time

from model.job.job import get_job, get_jobs
from model.job.create_job import create_job
from test.model.job import BaseTestJob


class TestGetJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_get_job(self):
        expected_job = create_job(company_id=self.company['_id'],
                                  title="title", description="description")
        job_id = expected_job['_id']

        job = get_job(job_id)

        self.assertEqual(expected_job, job)

    def test_get_job_invalid_id(self):
        create_job(company_id=self.company['_id'],
                   title="title", description="description")

        with self.assertRaises(ValueError):
            get_job(None)

        with self.assertRaises(ValueError):
            get_job("")

        with self.assertRaises(ValueError):
            get_job("valid id")

    @freeze_time("2015-10-26")
    def test_get_jobs(self):

        expected_job_1 = create_job(company_id=self.company['_id'],
                                    title="title", description="description")
        expected_job_2 = create_job(company_id=self.company['_id'],
                                    title="title", description="description")

        jobs = list(get_jobs())

        self.assertEqual(
            [expected_job_1['_id'], expected_job_2['_id']],
            [j['_id'] for j in jobs])

        self.assertEqual(
            [self.company['name'], self.company['name']],
            [j['company_name'] for j in jobs])

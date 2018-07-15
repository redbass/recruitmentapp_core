from datetime import datetime

from freezegun import freeze_time

from model.job.job import delete_jobs, get_job
from model.job.create_job import create_job
from test.model.job import BaseTestJob


class TestDeleteJobs(BaseTestJob):

    def test_delete_jobs(self):
        job = create_job(company_id=self.company['_id'],
                         title="title", description="description")
        job_id = job['_id']
        delete_jobs([job_id])

        stored_job = get_job(job_id)

        self.assertTrue(stored_job['deleted'])

    def test_delete_jobs_modified_date(self):

        with freeze_time("2015-10-26"):
            created_date = datetime.now()
            job = create_job(company_id=self.company['_id'],
                             title="title", description="description")

        with freeze_time("2015-10-27"):
            modified_date = datetime.now()
            job_id = job['_id']
            delete_jobs([job_id])

        stored_job = get_job(job_id)

        self.assertTrue(stored_job['deleted'])
        self.assertEqual(created_date, stored_job['date']['created'])
        self.assertEqual(modified_date, stored_job['date']['updated'])

    def test_delete_jobs_parameter_error(self):
        self.assertRaises(AttributeError, delete_jobs, None)
        self.assertRaises(AttributeError, delete_jobs, [])
        self.assertRaises(AttributeError, delete_jobs, '123')

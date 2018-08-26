from model.job.job import delete_jobs, get_job
from test.model.job import BaseTestJob, JobFactory


class TestDeleteJobs(BaseTestJob):

    def test_delete_jobs(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        delete_jobs([job_id])

        stored_job = get_job(job_id)

        self.assertTrue(stored_job['deleted'])

    def test_delete_jobs_parameter_error(self):
        self.assertRaises(AttributeError, delete_jobs, None)
        self.assertRaises(AttributeError, delete_jobs, [])
        self.assertRaises(AttributeError, delete_jobs, '123')

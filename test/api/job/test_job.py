from unittest.mock import patch

from api.routes.admin_routes import JOBS_URL, JOB_URL
from test.api import TestApi


class TestApiGetJobs(TestApi):

    @patch('api.job.job')
    def test_get_jobs(self, job):

        url = self.url_for_admin(JOBS_URL)
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        job.get_jobs.assert_called_once()

    @patch('api.job.job')
    def test_get_job(self, job):
        job_id = '123'

        url = self.url_for_admin(JOB_URL, job_id=job_id)
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        job.get_job.assert_called_once_with(job_id=job_id)

from json import loads
from unittest.mock import patch

from api.route import GET_JOB_URL, JOB_URL
from test.api import TestApi


class TestApiGetJob(TestApi):

    @patch('api.job.job')
    def test_get_jobs(self, job):
        job_id = '123'
        expected_job = {'_id': job_id, 'name': 'job'}
        job.get_jobs.return_value = [expected_job]

        url = self.url_for(GET_JOB_URL, _id=job_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.data), expected_job)

    @patch('api.job.job')
    def test_get_job_no_results(self, job):
        job_id = '123'
        job.get_jobs.return_value = []

        url = self.url_for(GET_JOB_URL, _id=job_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.data), [])


class TestApiCreateJob(TestApi):

    @patch('api.job.job')
    def test_create_job(self, job):

        data = {"title": "title",
                'description': 'description'}

        expected_job = {'result': 'result'}
        job.create_job.return_value = expected_job
        url = self.url_for(JOB_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(loads(response.data), expected_job)

    def test_create_job_no_input(self):
        url = self.url_for(JOB_URL)
        response = self.post_json(url, {})
        self.assertEqual(400, response.status_code)

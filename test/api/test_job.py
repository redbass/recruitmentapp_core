from json import loads
from unittest.mock import patch

from api.route import JOBS_URL
from test.api import TestApi


class TestApiCreateJob(TestApi):

    @patch('api.job.job')
    def test_create_job(self, job):
        title = 'title'
        description = 'description'
        data = {
            'title': title,
            'description': description
        }

        expected_job = {
            'result': 'result'}
        job.create_job.return_value = expected_job

        url = self.url_for(JOBS_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        job.create_job.assert_called_once_with(title, description, None)
        self.assertEqual(loads(response.data), expected_job)

    @patch('api.job.job')
    def test_create_job_with_location(self, job):
        title = 'title'
        description = 'description'
        location = {
            'latitude': 12.345,
            'longitude': 54.321
        }
        data = {
            'title': title,
            'description': description,
            'location': location
        }

        expected_job = {
            'result': 'result'}
        job.create_job.return_value = expected_job

        url = self.url_for(JOBS_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        call_args = job.create_job.call_args
        self.assertEqual(call_args[0][0], title)
        self.assertEqual(call_args[0][1], description)
        self.assertEqual(call_args[0][2].latitude, location['latitude'])
        self.assertEqual(call_args[0][2].longitude, location['longitude'])
        self.assertEqual(loads(response.data), expected_job)

    def test_create_job_no_input(self):
        url = self.url_for(JOBS_URL)
        response = self.post_json(url, {})
        self.assertEqual(400, response.status_code)

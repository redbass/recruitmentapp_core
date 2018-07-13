from json import loads
from unittest.mock import patch

from api.routes.admin_routes import JOBS_URL
from test.api import TestApi


class TestApiCreateJob(TestApi):

    @patch('api.job.job')
    def test_create_job(self, job):
        company_id = '123'
        title = 'title'
        description = 'description'
        data = {
            'company_id': company_id,
            'title': title,
            'description': description
        }

        expected_job = {
            'result': 'result'}
        job.create_job.return_value = expected_job

        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        job.create_job.assert_called_once_with(
            company_id=company_id,
            title=title,
            description=description,
            location=None)
        self.assertEqual(loads(response.data), expected_job)

    @patch('api.job.job')
    def test_create_job_with_location(self, job):
        company_id = '123'
        title = 'title'
        description = 'description'
        location = {
            'lat': 12.345,
            'lng': 54.321
        }
        data = {
            'company_id': company_id,
            'title': title,
            'description': description,
            'location': location
        }

        expected_job = {
            'result': 'result'}
        job.create_job.return_value = expected_job

        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        call_args = job.create_job.call_args
        self.assertEqual(call_args[1]['title'], title)
        self.assertEqual(call_args[1]['description'], description)
        self.assertEqual(call_args[1]['location'].latitude, location['lat'])
        self.assertEqual(call_args[1]['location'].longitude, location['lng'])
        self.assertEqual(loads(response.data), expected_job)

    def test_create_job_no_input(self):
        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, {})
        self.assertEqual(400, response.status_code)

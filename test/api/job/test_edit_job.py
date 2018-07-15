from json import loads
from unittest.mock import patch

from api.routes.admin_routes import JOB_URL
from model import NOT_PROVIDED
from test.api import TestApi


class EditJob(TestApi):

    @patch('api.job.edit_job')
    def test_edit_job(self, edit_job):
        job_id = '123'
        title = 'title'
        description = 'description'
        location = {
            'lat': 12.345,
            'lng': 54.321
        }
        data = {
            'title': title,
            'description': description,
            'location': location
        }

        expected_job = {'result': 'result'}
        edit_job.return_value = expected_job

        url = self.url_for_admin(JOB_URL, job_id=job_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        call_args = edit_job.call_args
        self.assertEqual(call_args[1]['new_title'], title)
        self.assertEqual(call_args[1]['new_description'], description)
        self.assertEqual(call_args[1]['new_location'].latitude,
                         location['lat'])
        self.assertEqual(call_args[1]['new_location'].longitude,
                         location['lng'])
        self.assertEqual(loads(response.data), expected_job)

    @patch('api.job.edit_job')
    def test_partial_edit_job(self, edit_job):
        edit_job.return_value = {'result': 'result'}
        job_id = '123'
        url = self.url_for_admin(JOB_URL, job_id=job_id)
        response = self.post_json(url, {})

        self.assertEqual(200, response.status_code)
        edit_job.assert_called_once_with(
            job_id=job_id,
            new_title=NOT_PROVIDED,
            new_description=NOT_PROVIDED,
            new_location=NOT_PROVIDED)
        self.assertEqual(loads(response.data), edit_job.return_value)

    @patch('api.job.edit_job')
    def test_invalid_location(self, _):
        job_id = '123'
        data = {'location': {'lat': 12.345}}

        url = self.url_for_admin(JOB_URL, job_id=job_id)

        response = self.post_json(url, data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(loads(response.data), {
            "exception": "ValueError",
            "message": "Provided invalid location: {'lat': 12.345}",
            "refId": ""
        })

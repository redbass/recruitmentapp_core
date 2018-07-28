from json import loads
from unittest.mock import patch

from api.routes.admin_routes import ADVERTS_URL, APPROVE_ADVERT_URL
from test.api import TestApi


class TestApiCreateAdvert(TestApi):

    @patch('api.advert.job_advert')
    def test_create_advert(self, job):
        job_id = '1'
        expected_duration = 10
        expected_response = {'response': job_id}

        job.create_advert_for_a_job.return_value = expected_response

        url = self.url_for_admin(ADVERTS_URL, job_id=job_id)
        data = {'duration': expected_duration}
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        job.create_advert_for_a_job.assert_called_once_with(
            job_id=job_id, advert_duration=expected_duration)

        self.assertEqual(expected_response, loads(response.data))

    def test_create_advert_with_invalid_duration(self):
        duration = "INVALID DURATION"
        url = self.url_for_admin(ADVERTS_URL, job_id="RANDOM")
        data = {'duration': duration}
        response = self.post_json(url, data)

        self.assert_error(response,
                          400,
                          "'{duration}' is not an integer duration"
                          .format(duration=duration))


class TestApiApproveAdvert(TestApi):

    @patch('api.advert.job_advert')
    def test_approve_advert(self, job):
        job_id = '1'
        advert_id = '1'

        url = self.url_for_admin(APPROVE_ADVERT_URL,
                                 job_id=job_id, advert_id=advert_id)
        response = self.post_json(url)

        self.assertEqual(200, response.status_code)
        job.approve_advert.assert_called_once_with(job_id=job_id,
                                                   advert_id=advert_id)

    @patch('api.advert.job_advert')
    def test_approve_advert_raise_error_if_not_in_draft(self, job):
        job.approve_advert.side_effect = ValueError("")
        url = self.url_for_admin(APPROVE_ADVERT_URL, job_id='1', advert_id='1')
        response = self.post_json(url)

        self.assertEqual(400, response.status_code)

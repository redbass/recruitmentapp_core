from datetime import datetime, timedelta
from json import loads
from unittest.mock import patch

from api.routes.admin_routes import ADVERTS_URL, APPROVE_ADVERT_URL
from test.api import TestApi


class TestApiCreateAdvert(TestApi):

    @patch('api.advert.job')
    def test_create_advert(self, job):
        job_id = '1'
        start_period = datetime.now()
        end_period = datetime.now() + timedelta(days=30)
        data = {
            'period': {
                'start': start_period.isoformat(),
                'end': end_period.isoformat(),
            }}

        expected_response = {
            'job_id': job_id}
        job.create_advert_for_a_job.return_value = expected_response

        url = self.url_for_admin(ADVERTS_URL, job_id=job_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        job.create_advert_for_a_job.assert_called_once_with(
            job_id=job_id, start_period=start_period, end_period=end_period)

        self.assertEqual(expected_response, loads(response.data))

    @patch('api.advert.job')
    def test_create_advert_without_start_date(self, job):
        periods = [
            {},
            {
                'start': ""},
            {
                'start': "asd"},
            {
                'start': datetime.now().isoformat(),
                'end': "asd"},
        ]
        for period in periods:
            job_id = 1
            data = {
                'period': period}
            url = self.url_for_admin(ADVERTS_URL, job_id=job_id)

            response = self.post_json(url, data)
            self.assertEqual(400, response.status_code)
            job.create_advert_for_a_job.assert_not_called()


class TestApiApproveAdvert(TestApi):

    @patch('api.advert.job')
    def test_approve_advert(self, job):
        job_id = '1'
        advert_id = '1'

        url = self.url_for_admin(APPROVE_ADVERT_URL,
                                 job_id=job_id, advert_id=advert_id)
        response = self.post_json(url)

        self.assertEqual(200, response.status_code)
        job.approve_advert.assert_called_once_with(job_id=job_id,
                                                   advert_id=advert_id)

    @patch('api.advert.job')
    def test_approve_advert_raise_error_if_not_in_draft(self, job):
        job.approve_advert.side_effect = ValueError("")
        url = self.url_for_admin(APPROVE_ADVERT_URL, job_id='1', advert_id='1')
        response = self.post_json(url)

        self.assertEqual(400, response.status_code)

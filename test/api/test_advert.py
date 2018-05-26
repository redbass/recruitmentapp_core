from datetime import datetime, timedelta
from json import loads
from unittest.mock import patch

from api.route import ADVERTS_URL
from test.api import TestApi


class TestApiCreateAdvert(TestApi):

    @patch('api.advert.create_advert_for_a_job')
    def test_create_advert(self, create_advert_for_a_job):
        job_id = '1'
        start_period = datetime.now()
        end_period = datetime.now() + timedelta(days=30)
        data = {'period': {
            'start': start_period.isoformat(),
            'end': end_period.isoformat(),
        }}

        expected_response = {'job_id': job_id}
        create_advert_for_a_job.return_value = expected_response

        url = self.url_for(ADVERTS_URL, job_id=job_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        create_advert_for_a_job\
            .assert_called_once_with(job_id=job_id,
                                     start_period=start_period,
                                     end_period=end_period)
        self.assertEqual(expected_response, loads(response.data))

    @patch('api.advert.create_advert_for_a_job')
    def test_create_advert_without_start_date(self, create_advert_for_a_job):
        periods = [
            {},
            {'start': ""},
            {'start': "asd"},
            {'start': datetime.now().isoformat(), 'end': "asd"},
        ]
        for period in periods:
            job_id = 1
            data = {'period': period}
            url = self.url_for(ADVERTS_URL, job_id=job_id)

            response = self.post_json(url, data)
            self.assertEqual(400, response.status_code)
            create_advert_for_a_job.assert_not_called()

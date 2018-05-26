import json

from freezegun import freeze_time

from api.route import JOBS_URL
from db.collections import jobs
from model.location import Location
from test_integration import IntegrationTestCase


@freeze_time("2015-10-26")
class TestCreateJob(IntegrationTestCase):

    def tearDown(self):
        super().tearDown()
        jobs.drop()

    def test_create_job(self):
        expected_data, response = self.create_job()

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNotNone(response_data.pop('_id'))
        self.assertEqual(response_data, expected_data)

    def create_job(self):
        title = 'The title'
        description = 'Job Description!'
        latitude = 12.345
        longitude = 54.321
        data = {
            'title': title,
            'description': description,
            'location': {
                'latitude': latitude,
                'longitude': longitude
            }
        }
        expected_data = {
            'title': title,
            'description': description,
            'location': Location(
                longitude=longitude, latitude=latitude).get_geo_json_point(),
            'deleted': False,
            'date': {
                'created': '2015-10-26T00:00:00',
                'updated': '2015-10-26T00:00:00',
            }
        }
        response = self.post_json(JOBS_URL, data)
        return expected_data, response

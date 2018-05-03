import json

from api.route import ADVERT_URL
from db.collections import adverts
from model.advert import create_advert, delete_adverts, get_adverts
from model.location import Location
from test_integration import IntegrationTestCase


class TestCreateAdvert(IntegrationTestCase):

    def tearDown(self):
        adverts.drop()

    def test_create_advert(self):
        title = 'The title'
        description = 'Advert Description!'

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
            'location': Location(longitude, latitude).get_geo_json_point(),
            'deleted': False,
            'draft': False,
            'period': {'start': None, 'stop': None},
         }

        response = self.post_json(ADVERT_URL, data)

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertIsNotNone(response_data.pop('_id'))
        self.assertEqual(response_data, expected_data)

    def test_delete_advert(self):
        advert = create_advert('title', 'description')

        delete_adverts([advert['_id']])

        deleted_adverts = get_adverts([advert['_id']])
        self.assertTrue(deleted_adverts[0].get('deleted'))

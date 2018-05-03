from json import loads
from unittest.mock import patch

from api.route import GET_ADVERT_URL, ADVERT_URL
from test.api import TestApi


class TestApiGetAdvert(TestApi):

    @patch('api.advert.advert')
    def test_get_advert(self, advert):
        advert_id = '123'
        expected_advert = {'_id': advert_id, 'name': 'advert'}
        advert.get_adverts.return_value = [expected_advert]

        url = self.url_for(GET_ADVERT_URL, _id=advert_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        advert.get_adverts.assert_called_once_with([advert_id])
        self.assertEqual(loads(response.data), expected_advert)

    @patch('api.advert.advert')
    def test_get_advert_no_results(self, advert):
        advert_id = '123'
        advert.get_adverts.return_value = []

        url = self.url_for(GET_ADVERT_URL, _id=advert_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        advert.get_adverts.assert_called_once_with([advert_id])
        self.assertEqual(loads(response.data), [])


class TestApiCreateAdvert(TestApi):

    @patch('api.advert.advert')
    def test_create_advert(self, advert):

        title = 'title'
        description = 'description'
        data = {
            'title': title,
            'description': description
        }

        expected_advert = {'result': 'result'}
        advert.create_advert.return_value = expected_advert

        url = self.url_for(ADVERT_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        advert.create_advert.assert_called_once_with(title, description, None)
        self.assertEqual(loads(response.data), expected_advert)

    @patch('api.advert.advert')
    def test_create_advert_with_location(self, advert):

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

        expected_advert = {'result': 'result'}
        advert.create_advert.return_value = expected_advert

        url = self.url_for(ADVERT_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        call_args = advert.create_advert.call_args
        self.assertEqual(call_args[0][0], title)
        self.assertEqual(call_args[0][1], description)
        self.assertEqual(call_args[0][2].latitude, location['latitude'])
        self.assertEqual(call_args[0][2].longitude, location['longitude'])
        self.assertEqual(loads(response.data), expected_advert)

    def test_create_advert_no_input(self):
        url = self.url_for(ADVERT_URL)
        response = self.post_json(url, {})
        self.assertEqual(400, response.status_code)

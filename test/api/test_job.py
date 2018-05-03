from json import loads
from unittest.mock import patch

from api.route import GET_ADVERT_URL, ADVERT_URL
from test.api import TestApi


class TestApiGetAdverts(TestApi):

    @patch('api.advert.advert')
    def test_get_adverts(self, advert):
        advert_id = '123'
        expected_advert = {'_id': advert_id, 'name': 'advert'}
        advert.get_adverts.return_value = [expected_advert]

        url = self.url_for(GET_ADVERT_URL, _id=advert_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.data), expected_advert)

    @patch('api.advert.advert')
    def test_get_advert_no_results(self, advert):
        advert_id = '123'
        advert.get_adverts.return_value = []

        url = self.url_for(GET_ADVERT_URL, _id=advert_id)
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.data), [])


class TestApiCreateAdvert(TestApi):

    @patch('api.advert.advert')
    def test_create_advert(self, advert):

        data = {"title": "title",
                'description': 'description'}

        expected_advert = {'result': 'result'}
        advert.create_advert.return_value = expected_advert
        url = self.url_for(ADVERT_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(loads(response.data), expected_advert)

    def test_create_advert_no_input(self):
        url = self.url_for(ADVERT_URL)
        response = self.post_json(url, {})
        self.assertEqual(400, response.status_code)

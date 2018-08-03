from json import loads
from unittest.mock import patch

from api.routes.routes import POSTCODE_SEARCH
from test.api import TestApi


class TestApiGetPostcode(TestApi):

    @patch('api.services.postcode.lib_get_postcode')
    def test_get_postcode(self, lib_get_postcode):
        expected_response = {"some": "data"}
        lib_get_postcode.return_value = {
            "result": expected_response,
            "status": 200
        }

        url = self.url_for(POSTCODE_SEARCH, postcode='eh88he')
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_response, loads(response.data))

    @patch('api.services.postcode.lib_get_postcode')
    def test_get_postcode_invalid_service_data(self, lib_get_postcode):
        lib_get_postcode.return_value = {"invalid": "data"}

        url = self.url_for(POSTCODE_SEARCH, postcode='eh88he')
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual({}, loads(response.data))

import json
from unittest.mock import patch

from api.route import SEARCH_ADVERTS_BY_RADIUS_URL
from test.api import TestApi


class TestAPISearchByArea(TestApi):

    @patch('api.search.job.search_adverts_by_radius')
    def test_search_advert_by_radius(self, search_by_radius):
        expected_data = [1, 2, 3]
        location = [12.345, 54.321]
        radius = 12
        search_by_radius.return_value = expected_data

        url_params = '?location={location}&radius={radius}'.format(
            location=location, radius=radius)

        url = SEARCH_ADVERTS_BY_RADIUS_URL + url_params
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)

        adverts = json.loads(response.data)
        self.assertEqual(adverts, expected_data)

        location_call = search_by_radius.call_args[0][0]
        radius_call = search_by_radius.call_args[0][1]
        self.assertEqual(location_call.latitude, location[0])
        self.assertEqual(location_call.longitude, location[1])
        self.assertEqual(radius_call, radius)

    def test_search_advert_with_location_as_less_then_2_values(self):
        self._assert_search_parameters(
            location=[12.345], radius=12,
            expected_msg_error='Invalid location format')

    def test_search_advert_with_location_as_more_then_2_values(self):
        self._assert_search_parameters(
            location=[12.345, 11.333, 44.555], radius=12,
            expected_msg_error='Invalid location format')

    def test_search_advert_with_null_location(self):
        self._assert_search_parameters(
            location='', radius=12,
            expected_msg_error='Invalid location format')

    def test_search_advert_with_letteral_location(self):
        self._assert_search_parameters(
            location='["asdfasdf","asdf"]', radius=12,
            expected_msg_error='Invalid location format')

    def test_search_advert_with_null_radius(self):
        self._assert_search_parameters(
            location='[12,34]', radius='',
            expected_msg_error='Invalid radius format')

    def test_search_advert_with_invalid_radius(self):
        self._assert_search_parameters(
            location='[12,34]', radius='aaa',
            expected_msg_error='Invalid radius format')

    def _assert_search_parameters(self, location, radius, expected_msg_error):
        url_params = '?location={location}&radius={radius}'.format(
            location=location, radius=radius)
        url = SEARCH_ADVERTS_BY_RADIUS_URL + url_params
        response = self.test_app.get(url)
        self.assertEqual(response.status_code, 400)
        error = json.loads(response.data)
        self.assertEqual(error['message'], expected_msg_error)

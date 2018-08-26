import json

from api.routes.routes import SEARCH_ADVERTS_BY_RADIUS_URL
from lib.geo import km2rad
from model.geo_location import get_location
from test.api import TestApi
from test.model.company import CompanyFactory
from test.model.job import JobFactory
from test.search import EDINBURGH_ZOO, EDINBURGH_EICA, EDINBURGH_CENTER


class TestAPISearchByArea(TestApi):

    def test_search_advert_by_radius(self):
        self._create_jobs()
        expected_jobs_id = [self.zoo_job['_id'], self.eica_job['_id']]
        coordinates = \
            get_location(**EDINBURGH_CENTER)['geo_location']['coordinates']
        radius = km2rad(15)

        url_params = '?location={location}&radius={radius}'.format(
            location=','.join(str(c) for c in coordinates), radius=radius)

        url = SEARCH_ADVERTS_BY_RADIUS_URL + url_params
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)

        adverts = json.loads(response.data)
        expected_job_ids = [a['_id'] for a in adverts]
        self.assertEqual(expected_jobs_id, expected_job_ids)

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

    def _create_jobs(self):
        self.zoo = self.create_from_factory(CompanyFactory, name="ZOO")
        self.zoo_job_input = self.load_example_model('create_job_input')
        self.zoo_job_input.update({
            'company_id': self.zoo['_id'],
            'title': "Breeder",
            'location': EDINBURGH_ZOO
        })
        self.zoo_job = self.create_from_factory(
            JobFactory, **self.zoo_job_input)

        self.eica = self.create_from_factory(CompanyFactory, name="EICA")
        self.eica_job_input = self.load_example_model('create_job_input')
        self.eica_job_input.update({
            'company_id': self.eica['_id'],
            'title': "Climber",
            'location': EDINBURGH_EICA
        })
        self.eica_job = self.create_from_factory(
            JobFactory, **self.eica_job_input)

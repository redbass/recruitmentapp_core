from db.collections import jobs, companies, users
from lib.geo import km2rad
from model.geo_location import get_location
from search.jobs import search_adverts_by_radius
from test import UnitTestCase
from test.model.company import CompanyFactory
from test.model.job import JobFactory

from test.search import EDINBURGH_CENTER, EDINBURGH_ZOO, EDINBURGH_EICA, \
    EDINBURGH_ROSELIN_CHAPEL


class SearchAdvertByRadiusTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.center_coordinates = \
            get_location(**EDINBURGH_CENTER)['geo_location']['coordinates']
        self._create_jobs()

    def tearDown(self):
        super().tearDown()
        jobs.drop()
        users.drop()
        companies.drop()

    def test_search_advert_by_radius_5km(self):
        rad = km2rad(6)
        results = search_adverts_by_radius(self.center_coordinates, rad)

        self.assertEqual(1, len(list(results)), 1)

    def test_search_advert_by_radius_11km(self):
        rad = km2rad(11)
        results = search_adverts_by_radius(self.center_coordinates, rad)

        self.assertEqual(2, len(list(results)))

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

        self.chapel = self.create_from_factory(CompanyFactory, name="Chapel")
        self.chapel_job_input = self.load_example_model('create_job_input')
        self.chapel_job_input.update({
            'company_id': self.chapel['_id'],
            'title': "Turist guide",
            'location': EDINBURGH_ROSELIN_CHAPEL
        })
        self.chapel_job = self.create_from_factory(
            JobFactory, **self.chapel_job_input)

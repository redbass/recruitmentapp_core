from db.collections import jobs
from lib.geo import km2rad
from model.job import create_job
from search.job import search_adverts_by_radius
from test import UnitTestCase

from test.search import EDINBURGH_CENTER, EDINBURGH_ZOO, \
    EDINBURGH_ROSELIN_CHAPEL


class SearchAdvertByRadiusTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self._create_jobs()

    def tearDown(self):
        super().tearDown()
        jobs.drop()

    def test_search_advert_by_radius_5km(self):
        rad = km2rad(6)
        results = search_adverts_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 1)

    def test_search_advert_by_radius_11km(self):
        rad = km2rad(11)
        results = search_adverts_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 2)

    def _create_jobs(self):
        self.edinburgh_center = create_job(
            "Edinburgh Zoo", "Edinburgh Zoo Description",
            EDINBURGH_ZOO)
        self.edinburgh_center = create_job(
            "Edinburgh Roselin chapel", "Edinburgh Roselin chapel Description",
            EDINBURGH_ROSELIN_CHAPEL)

from db.collections import adverts
from lib.geo import km2rad
from model.advert import create_advert
from search.advert import search_advert_by_radius
from test_integration import IntegrationTestCase
from test_integration.search import EDINBURGH_CENTER, EDINBURGH_ZOO, \
    EDINBURGH_ROSELIN_CHAPEL


class SearchAdvertByRadiusTestCase(IntegrationTestCase):

    def setUp(self):
        super().setUp()
        self._create_adverts()

    def tearDown(self):
        super().tearDown()
        adverts.drop()

    def test_search_advert_by_radius_5km(self):
        rad = km2rad(6)
        results = search_advert_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 1)

    def test_search_advert_by_radius_11km(self):
        rad = km2rad(11)
        results = search_advert_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 2)

    def _create_adverts(self):
        self.edinburgh_center = create_advert(
            "Edinburgh Zoo", "Edinburgh Zoo Description",
            EDINBURGH_ZOO)
        self.edinburgh_center = create_advert(
            "Edinburgh Roselin chapel", "Edinburgh Roselin chapel Description",
            EDINBURGH_ROSELIN_CHAPEL)

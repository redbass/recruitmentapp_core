from lib.geo import distance_from_location, \
    get_coordinates_from_location
from services.search import search
from test.services.search import EDINBURGH_CENTER, EDINBURGH_EICA, \
    STERLING_CASTLE, ITALY, BaseSearchTestCase

EARTH_RADIUS = 6371


class SearchByDistanceTestCase(BaseSearchTestCase):

    def setUp(self):
        super().setUp()

        self.current_location = get_coordinates_from_location(EDINBURGH_CENTER)

        self.guide = self._crate_job(
            title="Tourist guide Job", description="Description ten",
            location=EDINBURGH_EICA)

    def test_search_advert_by_radius_local_precision_500m(self):
        location = STERLING_CASTLE
        self._crate_job(
            title="Far job", description="Something Else", location=location)
        self._assert_search_by_location(location, 0.5)

    def test_search_advert_by_radius_italy_precision_5km(self):
        location = ITALY
        self._crate_job(
            title="Far FAR job", description="An Other", location=location)
        self._assert_search_by_location(location, 5)

    def _assert_search_by_location(self, test_location, delta_in_km):
        distance = distance_from_location(self.current_location,
                                          test_location)
        results_1 = search(query="Job", location=self.current_location,
                           distance=distance + delta_in_km)
        results_2 = search(query="Job", location=self.current_location,
                           distance=distance - delta_in_km)
        results_1 = list(results_1)
        results_2 = list(results_2)
        self.assertEquals(2, len(results_1))
        self.assertEquals(1, len(results_2))

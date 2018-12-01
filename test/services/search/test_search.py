from services.search import search
from test.services.search import BaseSearchTestCase, EDINBURGH_EICA, \
    EDINBURGH_ROSELIN_CHAPEL, EDINBURGH_ZOO


class SearchTestCase(BaseSearchTestCase):

    def setUp(self):
        super().setUp()

        self.guide = self._crate_job(
            title="Tourist guide Job", description="Description ten",
            location=EDINBURGH_ROSELIN_CHAPEL,
            metadata={'job_type': "wizard"})

        self.breeder = self._crate_job(
            title="Breeder job", description="Something Else",
            location=EDINBURGH_ZOO, rate={'type': 'salary'},
            medatada={'job_type': "software_tester"})

        self.climber = self._crate_job(
            title="Climber", description="Description eleven",
            location=EDINBURGH_EICA)

    def test_search_jobs_no_results(self):
        results, total, pages = search('NOTHING')
        self.assertEqual(0, len(results))
        self.assertEquals(0, total)
        self.assertEquals(0, pages)

    def test_search_return_total_results_and_pages(self):
        _, total, pages = search()
        self.assertEquals(3, total)
        self.assertEquals(1, pages)

    def test_search_return_no_results_if_requested_empty_page(self):
        results, total, pages = search(page=100)

        self.assertEquals(0, len(results))
        self.assertEquals(3, total)
        self.assertEquals(1, pages)

    def test_search_get_specific_page(self):
        results, total, pages = search(page=0, limit=2)

        self.assertEquals(2, len(results))
        self.assertEquals(3, total)
        self.assertEquals(2, pages)

        results, total, pages = search(page=1, limit=2)

        self.assertEquals(1, len(results))
        self.assertEquals(3, total)
        self.assertEquals(2, pages)

    def test_search_jobs_returns_hiring_managers_list_without_password(self):
        results, _, _ = search()

        for result in results:
            self.assertGreater(len(result['company']['hiring_managers']), 0)
            for hiring_manager in result['company']['hiring_managers']:
                self.assertIsNone(hiring_manager.get('password'))

    def test_search_jobs_by_job_type(self):
        self._assert_search(expected_jobs=[self.guide], job_type='wizard')

    def test_search_jobs_by_rate_type(self):
        self._assert_search(expected_jobs=[self.breeder],
                            rate_type='salary')

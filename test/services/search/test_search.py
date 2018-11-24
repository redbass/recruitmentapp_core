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
        results = list(search('NOTHING'))

        self.assertEqual(0, len(results))

    def test_search_jobs_returns_hiring_managers_list_without_password(self):
        results = list(search())

        for result in results:
            self.assertGreater(len(result['company']['hiring_managers']), 0)
            for hiring_manager in result['company']['hiring_managers']:
                self.assertIsNone(hiring_manager.get('password'))

    def test_search_jobs_by_job_type(self):
        self._assert_search(expected_jobs=[self.guide], job_type='wizard')

    def test_search_jobs_by_rate_type(self):
        self._assert_search(expected_jobs=[self.breeder],
                            rate_type='salary')

from services.search import search
from test.services.search import BaseSearchTestCase, \
    EDINBURGH_ROSELIN_CHAPEL, EDINBURGH_ZOO, EDINBURGH_EICA, ITALY


class SearchTextTestCase(BaseSearchTestCase):

    def setUp(self):
        super().setUp()

        self.guide = self._crate_job(
            title="Tourist guide Job", description="Description ten",
            location=EDINBURGH_ROSELIN_CHAPEL)

        self.breeder = self._crate_job(
            title="Breeder job", description="Something Else",
            location=EDINBURGH_ZOO)

        self.climber = self._crate_job(
            title="Climber", description="Description eleven",
            location=EDINBURGH_EICA)

        self.far_job = self._crate_job(
            title="Far Far away", description="this job is in italy",
            location=ITALY)

    def test_search_jobs_by_title(self):
        results = list(search('Job'))

        self.assertEqual(3, len(results))
        expected_jobs = [self.guide, self.breeder, self.far_job]

        self.assertEquals([j['title'] for j in expected_jobs],
                          [r['title'] for r in results])

    def test_search_jobs_by_description(self):
        results = list(search('Description'))

        self.assertEqual(2, len(results))
        expected_jobs = [self.guide, self.climber]

        self.assertEquals([j['title'] for j in expected_jobs],
                          [r['title'] for r in results])

    def test_search_jobs_by_title_and_description(self):
        results = list(search('breeder eleven'))

        self.assertEqual(2, len(results))
        self.assertEqual(self.climber['title'], results[0]['title'])
        self.assertEqual(self.breeder['title'], results[1]['title'])

    def test_search_jobs_by_lowercase(self):
        results = list(search('climber'))

        self.assertEqual(1, len(results))
        self.assertEqual(self.climber['title'], results[0]['title'])

    def test_search_jobs_no_results(self):
        results = list(search('NOTHING'))

        self.assertEqual(0, len(results))

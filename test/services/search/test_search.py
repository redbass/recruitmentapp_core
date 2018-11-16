from db.collections import _create_text_index
from services.search import search
from test.services.search import BaseSearchTestCase, \
    EDINBURGH_ROSELIN_CHAPEL, EDINBURGH_ZOO, EDINBURGH_EICA, ITALY, \
    EDINBURGH_ARTHURS_SEAT


class SearchTextTestCase(BaseSearchTestCase):

    def setUp(self):
        super().setUp()
        _create_text_index()

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

        self.expiredJob = self._crate_job(
            title="Expired Job", description="This is an expired job",
            location=EDINBURGH_EICA,
            expired=True)

        self.job_not_publish = self._crate_job(
            title="Climber", description="Description eleven",
            location=EDINBURGH_ARTHURS_SEAT,
            published=False
        )

    def test_search_with_no_params_return_all_approved_not_expired(self):
        expected_jobs = [self.guide, self.breeder, self.climber, self.far_job]
        self._assert_search(expected_jobs=expected_jobs)

    def test_search_jobs_by_title(self):
        expected_jobs = [self.guide, self.breeder, self.far_job]
        self._assert_search(expected_jobs=expected_jobs,
                            query='Job')

    def test_search_jobs_by_description(self):
        expected_jobs = [self.climber, self.guide]

        self._assert_search(expected_jobs=expected_jobs,
                            comparator='description',
                            query='Description')

    def test_search_jobs_by_title_and_description(self):
        expected_jobs = [self.climber, self.breeder]

        self._assert_search(expected_jobs=expected_jobs,
                            query='breeder eleven')

    def test_search_jobs_by_lowercase(self):
        expected_jobs = [self.climber]

        self._assert_search(expected_jobs=expected_jobs,
                            query='climber')

    def test_search_jobs_no_results(self):
        results = list(search('NOTHING'))

        self.assertEqual(0, len(results))

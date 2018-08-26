from db.collections import companies, users, jobs, _create_text_index
from search.jobs import search
from test import UnitTestCase
from test.model.job import JobFactory


class TestSearchJobs(UnitTestCase):

    def setUp(self):
        super().setUp()
        _create_text_index()

        self.job_1 = self.create_from_factory(
            JobFactory, title="Title one", description="Description ten")

        self.job_2 = self.create_from_factory(
            JobFactory, title="Title two", description="Something Else")

        self.job_3 = self.create_from_factory(
            JobFactory, title="Tree", description="Description eleven")

    def tearDown(self):
        companies.drop()
        users.drop()
        jobs.drop()
        super().tearDown()

    def test_search_jobs_by_title(self):
        results = list(search('Title'))

        self.assertEqual(2, len(results))
        self.assertEqual(self.job_1['_id'], results[0]['_id'])
        self.assertEqual(self.job_2['_id'], results[1]['_id'])

    def test_search_jobs_by_description(self):
        results = list(search('Description'))

        self.assertEqual(2, len(results))
        self.assertEqual(self.job_1['_id'], results[0]['_id'])
        self.assertEqual(self.job_3['_id'], results[1]['_id'])

    def test_search_jobs_by_title_and_description(self):
        results = list(search('two eleven'))

        self.assertEqual(2, len(results))
        self.assertEqual(self.job_2['_id'], results[0]['_id'])
        self.assertEqual(self.job_3['_id'], results[1]['_id'])

    def test_search_jobs_by_lowercase(self):
        results = list(search('tree'))

        self.assertEqual(1, len(results))
        self.assertEqual(self.job_3['_id'], results[0]['_id'])

    def test_search_jobs_no_results(self):
        results = list(search('NOTHING'))

        self.assertEqual(0, len(results))

from db.collections import companies, users, jobs, _create_text_index
from model.company.company import create_company
from model.job.create_job import create_job
from model.user import create_user, UserType
from search.jobs import search
from test import UnitTestCase


class TestSearchJobs(UnitTestCase):

    def setUp(self):
        super().setUp()
        _create_text_index()
        self.admin = create_user(username="user_1",
                                 email="email@test.it",
                                 password="password",
                                 user_type=UserType.ADMIN)

        self.company = create_company(name='Company A',
                                      admin_user_ids=[self.admin['_id']],
                                      description='')

        self.job_1 = create_job(company_id=self.company['_id'],
                                title="Title one",
                                description="Description ten")

        self.job_2 = create_job(company_id=self.company['_id'],
                                title="Title two",
                                description="Something Else")

        self.job_3 = create_job(company_id=self.company['_id'],
                                title="Tree",
                                description="Description eleven")

    def tearDown(self):
        companies.drop()
        users.drop()
        job_ids = [j['_id'] for j in [self.job_1, self.job_2, self.job_3]]
        jobs.delete_many({
            '_id': {
                '$in': job_ids}
        })
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

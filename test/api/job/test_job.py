from api.routes.admin_routes import JOBS_URL, JOB_URL
from json import loads
from api.routes.hm_routes import COMPANY_JOBS_URL
from test.api.job import BaseTestApiJob
from test.model.company import CompanyFactory
from test.model.job import JobFactory


class TestApiGetJobs(BaseTestApiJob):

    def test_get_jobs(self):
        job_1, job_2, job_3, job_4 = self._create_jobs()
        expected_jobs = [job_1, job_2, job_3, job_4]

        url = self.url_for_admin(JOBS_URL)
        self._assert_get_jobs(expected_jobs, url)

    def test_get_company_jobs(self):
        job_1, job_2, _, ___ = self._create_jobs()
        expected_jobs = [job_1, job_2]

        url = self.url_for(COMPANY_JOBS_URL)
        self._assert_get_jobs(expected_jobs, url)

    def test_get_job(self):
        expected_job, _, __, ___ = self._create_jobs()

        url = self.url_for_admin(JOB_URL, job_id=expected_job['_id'])
        response = self.get_json(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_job['_id'], loads(response.data)['_id'])

    def _create_jobs(self):
        company_1 = self._company
        company_2 = self.create_from_factory(CompanyFactory)
        job_1 = self.create_from_factory(JobFactory,
                                         company_id=company_1['_id'])
        job_2 = self.create_from_factory(JobFactory,
                                         company_id=company_1['_id'])
        job_3 = self.create_from_factory(JobFactory,
                                         company_id=company_2['_id'])
        job_4 = self.create_from_factory(JobFactory,
                                         company_id=company_2['_id'])
        return job_1, job_2, job_3, job_4

    def _assert_get_jobs(self, expected_jobs, url):
        response = self.get_json(url)
        self.assertEqual(200, response.status_code)
        result_jobs = loads(response.data)
        self.assertEqual([j['_id'] for j in expected_jobs],
                         [j['_id'] for j in result_jobs])

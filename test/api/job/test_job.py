from api.routes.admin_routes import JOBS_URL, JOB_URL
from json import loads
from api.routes.hm_routes import COMPANY_JOBS_URL
from model.job.job_advert import request_approval_job_advert, add_advert_to_job
from model.job import AdvertStatus
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
        response = self.get_data(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_job['_id'], loads(response.data)['_id'])

    def test_get_jobs_with_request_approve_adverts(self):
        job_1, job_2, job_3, job_4 = self._create_jobs()
        self._request_advert_approval(job_1['_id'])
        self._request_advert_approval(job_3['_id'])

        expected_jobs = [job_1, job_3]

        filter_param = '?advertsStatusFilter={status}'\
            .format(status=AdvertStatus.REQUEST_APPROVAL)
        url = self.url_for_admin(JOBS_URL + filter_param)
        self._assert_get_jobs(expected_jobs, url)

    def test_get_jobs_exclude_drafts(self):
        job_1, job_2, job_3, job_4 = self._create_jobs()
        self._add_advert(job_2['_id'])
        self._add_advert(job_4['_id'])
        self._request_advert_approval(job_1['_id'])
        self._request_advert_approval(job_3['_id'])

        expected_jobs = [job_1, job_3]

        filter_param = '?excludeDrafts={exclude}'\
            .format(exclude=True)
        url = self.url_for_admin(JOBS_URL + filter_param)
        self._assert_get_jobs(expected_jobs, url)

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
        response = self.get_data(url)
        self.assertEqual(200, response.status_code)
        result_jobs = loads(response.data)
        self.assertEqual([j['_id'] for j in expected_jobs],
                         [j['_id'] for j in result_jobs])

    def _request_advert_approval(self, job_id):
        advert = self._add_advert(job_id)
        request_approval_job_advert(job_id=job_id, advert_id=advert['_id'])

    def _add_advert(self, job_id):
        advert = add_advert_to_job(job_id=job_id, advert_duration_days=10)
        return advert

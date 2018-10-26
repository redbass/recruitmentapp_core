from json import loads

from api.routes.admin_routes import JOBS_URL, JOB_URL, ADVERTS_URL, \
    SET_ADVERT_STATUS_URL
from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, AdvertStatus, \
    approve_job_advert
from test.api.job import BaseTestApiJob
from test.model.company import CompanyFactory
from test.model.job import JobFactory


class TestApiCreateJob(BaseTestApiJob):

    def setUp(self):
        super().setUp()
        self.company = self.create_from_factory(CompanyFactory)

    def test_create_job(self):

        job_input = self.load_example_model('create_job_input')
        job_input['company_id'] = self.company['_id']

        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, job_input)

        self.assertEqual(200, response.status_code)
        created_job = loads(response.data)
        stored_job = get_job(created_job['_id'])

        self.assertEqual(created_job, stored_job)
        self.assertEqual(job_input['title'], stored_job['title'])
        self.assertEqual(self.company['_id'], stored_job['company_id'])

    def test_create_job_invalid_company_id(self):
        job_input = self.load_example_model('create_job_input')

        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, job_input)

        self.assertEqual(400, response.status_code)
        self.assertEqual(loads(response.data), {
            "exception": "ValueError",
            "message": "The company_id `1234123412341234` is invalid",
            "refId": ""
        })

    def test_create_job_invalid_data(self):
        job_input = self.load_example_model('create_job_input')
        job_input['duration_days'] = "SOME RANDOM STRING"

        url = self.url_for_admin(JOBS_URL)
        response = self.post_json(url, job_input)

        self.assertEqual(400, response.status_code)
        self.assertEqual(loads(response.data), {
            "exception": "ValidationError",
            "message": "'SOME RANDOM STRING' is not of type 'integer'",
            "refId": ""
        })


class TestEditJob(BaseTestApiJob):

    def setUp(self):
        super().setUp()
        self.job = self.create_from_factory(JobFactory)

    def test_edit_job(self):

        data = {"title": "new title"}
        job_id = self.job['_id']

        url = self.url_for_admin(JOB_URL, job_id=job_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        result_job = get_job(job_id)

        self.assertEqual(data['title'], result_job['title'])
        self.assertEqual(self.job['description'], result_job['description'])

    def test_invalid_input(self):
        data = {"company_id": "RANDOM"}
        job_id = self.job['_id']
        expected_response = {
            "exception": "ValidationError",
            "message": "{'company_id': 'RANDOM'} is not valid under any "
                       "of the given schemas",
            "refId": ""
        }

        url = self.url_for_admin(JOB_URL, job_id=job_id)
        response = self.post_json(url, data)

        self.assertEqual(400, response.status_code)
        self.assertEqual(expected_response, loads(response.data))


class TestJobAdvert(BaseTestApiJob):

    def setUp(self):
        super().setUp()
        self.job = self.create_from_factory(JobFactory)
        self.job_id = self.job['_id']
        self.advert = add_advert_to_job(job_id=self.job_id,
                                        advert_duration_days=15)

    def test_api_add_advert_to_job(self):
        expected_duration = 10

        url = self.url_for_admin(ADVERTS_URL, job_id=self.job_id)
        data = {'duration': expected_duration}

        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        stored_job = get_job(job_id=self.job_id)

        self.assertEquals(AdvertStatus.DRAFT,
                          stored_job['adverts'][0]['status'])

    def test_api_add_advert_to_job_return_error_invalid_duration(self):
        duration = "INVALID DURATION"
        url = self.url_for_admin(ADVERTS_URL, job_id="RANDOM")
        data = {'duration': duration}
        response = self.post_json(url, data)

        self.assert_error(response,
                          400,
                          "'{duration}' is not a valid duration"
                          .format(duration=duration))

    def test_approve_advert(self):
        self._assert_set_status(action="approve",
                                expected_action=AdvertStatus.APPROVED)

    def test_pay_advert(self):
        approve_job_advert(job_id=self.job_id, advert_id=self.advert['_id'])

        self._assert_set_status(action="pay",
                                expected_action=AdvertStatus.PAYED)

    def test_publish_advert(self):
        approve_job_advert(job_id=self.job_id, advert_id=self.advert['_id'])

        self._assert_set_status(action="publish",
                                expected_action=AdvertStatus.PUBLISHED)

    def _assert_set_status(self, action, expected_action):
        url = self.url_for_admin(SET_ADVERT_STATUS_URL,
                                 job_id=self.job_id,
                                 advert_id=self.advert['_id'],
                                 action=action)
        response = self.post_json(url)
        self.assertEqual(200, response.status_code)
        stored_job = get_job(job_id=self.job_id)
        self.assertEquals(expected_action,
                          stored_job['adverts'][0]['status'])

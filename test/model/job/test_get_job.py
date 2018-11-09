from freezegun import freeze_time

from model.job.job import get_job, get_jobs
from model.job.job_advert import request_approval_job_advert, \
    add_advert_to_job, AdvertStatus
from test.model.company import CompanyFactory
from test.model.job import BaseTestJob, JobFactory


class TestGetJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_get_job(self):
        expected_job = self.create_from_factory(JobFactory)
        job_id = expected_job['_id']

        job = get_job(job_id)

        self.assertEqual(expected_job, job)

    def test_get_job_invalid_id(self):
        self.create_from_factory(JobFactory)

        with self.assertRaises(ValueError):
            get_job(None)

        with self.assertRaises(ValueError):
            get_job("")

        with self.assertRaises(ValueError):
            get_job("valid id")

    @freeze_time("2015-10-26")
    def test_get_jobs(self):
        company = self.create_from_factory(CompanyFactory)
        expected_job_1 = self.create_from_factory(JobFactory, title="Title 1",
                                                  company_id=company['_id'])
        expected_job_2 = self.create_from_factory(JobFactory, title="Title 2",
                                                  company_id=company['_id'])

        jobs = list(get_jobs())

        self.assertEqual(
            [expected_job_1['_id'], expected_job_2['_id']],
            [j['_id'] for j in jobs])

        self.assertEqual(
            [company['name'], company['name']],
            [j['company_name'] for j in jobs])

    def test_get_company_jobs(self):
        company_1 = self.create_from_factory(CompanyFactory)
        company_2 = self.create_from_factory(CompanyFactory)
        company_1_id = company_1['_id']

        job_1 = self.create_from_factory(JobFactory, title="Title 1",
                                         company_id=company_1_id)
        self.create_from_factory(JobFactory, title="Title 1",
                                 company_id=company_2['_id'])
        job_3 = self.create_from_factory(JobFactory, title="Title 1",
                                         company_id=company_1_id)
        self.create_from_factory(JobFactory, title="Title 1",
                                 company_id=company_2['_id'])

        expected_jobs = [job_1, job_3]

        jobs = list(get_jobs(company_1_id))

        self.assertEqual([j['_id'] for j in expected_jobs],
                         [j['_id'] for j in jobs])

    def test_get_jobs_filtered_by_advert_type(self):
        job_1, advert1 = self._create_job_with_advert()
        _, __ = self._create_job_with_advert()
        job_3, advert3 = self._create_job_with_advert()

        request_approval_job_advert(job_id=job_1['_id'],
                                    advert_id=advert1['_id'])
        request_approval_job_advert(job_id=job_3['_id'],
                                    advert_id=advert3['_id'])

        expected_job_ids = [job_1['_id'], job_3['_id']]

        jobs = get_jobs(adverts_status_filter=AdvertStatus.REQUEST_APPROVAL)

        self.assertEquals(expected_job_ids, [j['_id'] for j in list(jobs)])

    def _create_job_with_advert(self):
        job = self.create_from_factory(JobFactory)
        advert = add_advert_to_job(job_id=job['_id'], advert_duration_days=10)
        return job, advert

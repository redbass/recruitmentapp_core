from datetime import datetime

from model.advert import AdvertStatus
from model.job import create_job, create_advert_for_a_job, approve_advert, \
    get_job
from test.model.job import BaseTestJob


class TestCreateJob(BaseTestJob):

    def test_create_job(self):
        job = create_job(company_id=self.company['_id'],
                         title='Title', description='Description')
        advert = create_advert_for_a_job(job_id=job['_id'],
                                         start_period=datetime.now())
        approve_advert(job_id=job['_id'], advert_id=advert['_id'])

        job = get_job(job['_id'])

        self.assertEqual(job['adverts'][0]['status'], AdvertStatus.APPROVED)

    def test_create_job_wrong_job_id(self):
        job = create_job(company_id=self.company['_id'],
                         title='Title', description='Description')
        advert = create_advert_for_a_job(job_id=job['_id'],
                                         start_period=datetime.now())

        with self.assertRaises(ValueError):
            approve_advert(job_id=None, advert_id=None)
            approve_advert(job_id=None, advert_id=advert['_id'])
            approve_advert(job_id="WRONG", advert_id=advert['_id'])
            approve_advert(job_id=job['_id'], advert_id=None)
            approve_advert(job_id=job['_id'], advert_id='WRONG')

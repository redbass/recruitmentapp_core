from json import loads

from api.routes.routes import STRIPE_CHARGE_PROCESSED
from db.collections import payments
from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    AdvertStatus, pay_job_advert
from test.api.job import BaseTestApiJob
from test.features import crate_stripe_charge_response
from test.model.job import JobFactory


class TestApiStripeChargeProcessed(BaseTestApiJob):

    def test_stripe_charge_processed(self):

        job_id, advert_id = self._create_payed_advert()

        stripe_charge_response = crate_stripe_charge_response(
            job_id=job_id, advert_id=advert_id)

        url = self.url_for(STRIPE_CHARGE_PROCESSED)
        response = self.post_json(url, stripe_charge_response)

        self.assertEqual(200, response.status_code)

        payment_response = loads(response.data)
        payment_id = payment_response['payment_id']

        self.assertEquals(1, payments.find({'_id': payment_id}).count())

        stored_adverts = self._get_stored_adverts(job_id)
        self.assertEquals(AdvertStatus.PUBLISHED, stored_adverts[0]['status'])

    def _create_payed_advert(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']
        approve_job_advert(job_id=job_id, advert_id=advert_id)
        pay_job_advert(job_id=job_id, advert_id=advert_id)
        return job_id, advert_id

    def _get_stored_adverts(self, job_id):
        stored_job = get_job(job_id=job_id)
        job_adverts = stored_job['adverts']
        return job_adverts

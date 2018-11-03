from json import loads

from api.routes.routes import STRIPE_WEBHOOK_CHARGE
from db.collections import payments
from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    AdvertStatus
from test.api.job import BaseTestApiJob
from test.features import crate_stripe_charge_response
from test.model.job import JobFactory


class TestApiPublishByStripePayment(BaseTestApiJob):

    def test_publish_payed_advert(self):

        job_id, advert_id = self._create_advert()

        stripe_charge_response = crate_stripe_charge_response(
            job_id=job_id, advert_id=advert_id)

        url = self.url_for(STRIPE_WEBHOOK_CHARGE)
        response = self.post_json(url, stripe_charge_response)

        self.assertEqual(200, response.status_code)

        payment_response = loads(response.data)
        payment_id = payment_response['payment_id']

        self.assertEquals(1, payments.find({'_id': payment_id}).count())

        stored_job = get_job(job_id=job_id)
        job_adverts = stored_job['adverts']
        self.assertEquals(1, len(job_adverts))
        self.assertEquals(AdvertStatus.PUBLISHED, job_adverts[0]['status'])

    def _create_advert(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)

        advert_id = advert['_id']
        approve_job_advert(job_id=job_id, advert_id=advert_id)

        return job_id, advert_id

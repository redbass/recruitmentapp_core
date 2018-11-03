from db.collections import payments
from integrations.stripe import publish_payed_advert
from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    pay_job_advert, AdvertStatus
from test.api.job import BaseTestApiJob
from test.features import crate_stripe_charge_response
from test.model.job import JobFactory


class TestStripeIntegration(BaseTestApiJob):

    def test_publish_payed_advert(self):
        job_id, advert_id = self._create_payed_advert()
        stripe_charge_payload = crate_stripe_charge_response(
            job_id=job_id, advert_id=advert_id)

        payment_id = publish_payed_advert(stripe_charge_payload)

        self.assertEquals(1, payments.find({'_id': payment_id}).count())

        stored_adverts = self._get_stored_adverts(job_id)
        self.assertEquals(AdvertStatus.PUBLISHED, stored_adverts[0]['status'])

    def test_publish_payed_advert_of_unpaid_advert(self):
        job_id, advert_id, charge_payload = self._create_approved_advert()

        with self.assertRaises(ValueError):
            publish_payed_advert(charge_payload)

    def _create_approved_advert(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']
        approve_job_advert(job_id=job_id, advert_id=advert_id)

        charge_payload = crate_stripe_charge_response(
            job_id=job_id, advert_id=advert_id)

        return job_id, advert_id, charge_payload

    def _create_payed_advert(self):
        job_id, advert_id, charge_payload = self._create_approved_advert()
        pay_job_advert(job_id=job_id, advert_id=advert_id)
        return job_id, advert_id

    def _get_stored_adverts(self, job_id):
        stored_job = get_job(job_id=job_id)
        return stored_job['adverts']

import json
from unittest.mock import patch

from api.routes.routes import STRIPE_CHARGE_PROCESSED, STRIPE_CHARGE_PAYMENT
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    pay_job_advert, request_approval_job_advert
from test.api.job import BaseTestApiJob
from test.model.job import JobFactory


class TestApiStripeIntegration(BaseTestApiJob):

    @patch('api.integration.stripe.pay_job_advert')
    def test_charge_payment(self, pay_job_advert_mock):

        job_id, advert_id = self._create_payed_advert()
        token = "this is a token"

        url = self.url_for(STRIPE_CHARGE_PAYMENT)
        data = {
            'job_id': job_id,
            'advert_id': advert_id,
            'token': token
        }
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        pay_job_advert_mock.assert_called_with(
            advert_id=advert_id, job_id=job_id, stripe_token=token)

        response_data = json.loads(response.data)
        self.assertEquals(job_id, response_data['job']['_id'])

    @patch('api.integration.stripe.publish_payed_advert')
    def test_stripe_charge_processed(self, publish_payed_advert_mock):
        payment_id = "payment id"
        publish_payed_advert_mock.return_value = payment_id
        stripe_payload = {'value': "this is a random value"}

        url = self.url_for(STRIPE_CHARGE_PROCESSED)
        response = self.post_json(url, stripe_payload)

        self.assertEqual(200, response.status_code)

        publish_payed_advert_mock.assert_called_with(
            stripe_payload=stripe_payload)

    def _create_payed_advert(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']
        request_approval_job_advert(job_id=job_id, advert_id=advert_id)
        approve_job_advert(job_id=job_id, advert_id=advert_id)
        pay_job_advert(job_id=job_id, advert_id=advert_id)
        return job_id, advert_id

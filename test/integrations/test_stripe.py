from unittest.mock import patch

from db.collections import payments, configs
from exceptions.stripe import StripeException
from integrations.stripe import publish_payed_advert, pay_job_advert
from model.job.job_advert import pay_job_advert as pay_advert, \
    request_approval_job_advert
from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    AdvertStatus
from test.api.job import BaseTestApiJob
from test.features import crate_stripe_charge_response
from test.model.job import JobFactory


class MockStripeCharge:

    def __init__(self, response_status) -> None:
        self.status = response_status
        self.failure_message = "Some failure message"


class BaseTestIntegrationStripe(BaseTestApiJob):

    def setUp(self):
        super().setUp()
        self.token = "some random token"
        self.default_advert_charge = 123
        self.default_currency = 'EUR'
        self.default_charge_description = 'this is an advert'
        self._store_stripe_settings()

    def _create_approved_advert(self):
        job = self.create_from_factory(JobFactory)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']
        request_approval_job_advert(job_id=job_id, advert_id=advert_id)
        approve_job_advert(job_id=job_id, advert_id=advert_id)

        return job_id, advert_id

    def _get_stored_adverts(self, job_id):
        stored_job = get_job(job_id=job_id)
        return stored_job['adverts']

    def _store_stripe_settings(self):
        conf = {
            'default_advert_charge': self.default_advert_charge,
            'default_currency': self.default_currency,
            'default_charge_description': self.default_charge_description,
        }
        configs.update_one({'_id': 'stripe'},
                           {'$set': conf},
                           upsert=True)


class TestPayJobAdvert(BaseTestIntegrationStripe):

    @patch('integrations.stripe.stripe')
    def test_pay_advert(self, stripe_mock):
        response_status = 'succeeded'
        stored_advert, _, __ = self._call_publish_advert(response_status,
                                                         stripe_mock)
        self.assertEquals(stored_advert['status'], AdvertStatus.PAYED)

    @patch('integrations.stripe.stripe')
    def test_pay_advert_raises_exception_on_stripe_error(self, stripe_mock):
        response_status = 'not succeeded'
        with self.assertRaises(StripeException):
            stored_advert, _, __ = self._call_publish_advert(response_status,
                                                             stripe_mock)
            self.assertEquals(stored_advert['status'], AdvertStatus.APPROVED)

    @patch('integrations.stripe.stripe')
    def test_pay_advert_call_stripe(self, stripe_mock):
        stored_advert, job_id, advert_id = \
            self._call_publish_advert('succeeded', stripe_mock)
        stripe_mock.Charge.create.assert_called_with(
            amount=self.default_advert_charge,
            currency=self.default_currency,
            description=self.default_charge_description,
            source=self.token,
            metadata={
                'job_id': job_id,
                'advert_id': advert_id
            }
        )

    def _call_publish_advert(self, response_status, stripe_mock):
        job_id, advert_id = self._create_approved_advert()
        charge = MockStripeCharge(response_status=response_status)
        stripe_mock.Charge.create.return_value = charge
        pay_job_advert(advert_id=advert_id, job_id=job_id,
                       stripe_token=self.token)
        stored_advert = self._get_stored_adverts(job_id)[0]
        return stored_advert, job_id, advert_id


class TestPublishPayedAdvert(BaseTestIntegrationStripe):

    def test_publish_payed_advert(self):
        job_id, advert_id = self._create_payed_advert()
        stripe_payload = crate_stripe_charge_response(job_id=job_id,
                                                      advert_id=advert_id)
        payment_id = publish_payed_advert(stripe_payload=stripe_payload)

        stored_payment = payments.find_one({
                                               '_id': payment_id})
        stored_adverts = self._get_stored_adverts(job_id=job_id)

        self.assertIsNotNone(stored_payment)
        self.assertEquals(stored_adverts[0]['_id'], advert_id)
        self.assertEquals(stored_adverts[0]['status'], AdvertStatus.PUBLISHED)

    def test_publish_payed_wrong_payload_raise_exception(self):
        with self.assertRaises(ValueError):
            publish_payed_advert({})

    def _create_payed_advert(self):
        job_id, advert_id = self._create_approved_advert()
        pay_advert(job_id=job_id, advert_id=advert_id)
        return job_id, advert_id

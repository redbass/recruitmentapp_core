from db.collections import payments
from model.payment import store_payment
from test import UnitTestCase
from test.features import crate_stripe_charge_response

STRIPE_CHARGE_RESPONSE = crate_stripe_charge_response()


class TestPayAdverts(UnitTestCase):

    def setUp(self):
        super().setUp()
        response_object = STRIPE_CHARGE_RESPONSE['data']['object']

        self.payment_id = response_object['id']
        self.job_id = response_object['metadata']['job_id']
        self.advert_id = response_object['metadata']['advert_id']

    def test_store_payment(self):
        payment_id, job_id, advert_id = store_payment(STRIPE_CHARGE_RESPONSE)

        stored_payment = payments.find_one({'_id': self.payment_id})
        stored_content = stored_payment['content']

        self.assertEquals(self.payment_id, payment_id)
        self.assertEquals(self.job_id, job_id)
        self.assertEquals(self.advert_id, advert_id)
        self.assertEquals(STRIPE_CHARGE_RESPONSE, stored_content)

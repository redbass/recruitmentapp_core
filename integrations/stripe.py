import stripe

from config import settings
from exceptions.stripe import StripeException
from model.job.job_advert import publish_payed_job_advert, \
    pay_job_advert as pay_advert
from model.payment import store_payment

DEFAULT_CURRENCY = 'GBP'
DEFAULT_ADVERT_CHARGE = 2000
DEFAULT_CHARGE_DESCRIPTION = 'Single Payment'

stripe.api_key = settings.STRIPE_SECRET_KEY


def pay_job_advert(job_id, advert_id, stripe_token):

    response = stripe.Charge.create(
        amount=DEFAULT_ADVERT_CHARGE,
        currency=DEFAULT_CURRENCY,
        description=DEFAULT_CHARGE_DESCRIPTION,
        source=stripe_token,
        metadata={
            'job_id': job_id,
            'advert_id': advert_id
        }
    )

    if response.status != 'succeeded':
        raise StripeException(response.failure_message)

    pay_advert(advert_id=advert_id, job_id=job_id)


def publish_payed_advert(stripe_payload):
    try:
        response_object = stripe_payload['data']['object']

        payment_id = response_object['id']
        job_id = response_object['metadata']['job_id']
        advert_id = response_object['metadata']['advert_id']
    except KeyError:
        raise ValueError("The provided stripe payload is not valid")

    store_payment(payment_id=payment_id, payment_content=stripe_payload)
    publish_payed_job_advert(job_id=job_id, advert_id=advert_id)

    return payment_id

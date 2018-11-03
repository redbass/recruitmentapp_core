from model.job.job_advert import publish_payed_job_advert
from model.payment import store_payment


def publish_payed_advert(stripe_payload):
    response_object = stripe_payload['data']['object']

    payment_id = response_object['id']
    job_id = response_object['metadata']['job_id']
    advert_id = response_object['metadata']['advert_id']

    store_payment(payment_id=payment_id, payment_content=stripe_payload)
    publish_payed_job_advert(job_id=job_id, advert_id=advert_id)

    return payment_id

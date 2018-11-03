from flask import request
from flask.json import jsonify

from auth.api_token import api_token_required
from model.job.job_advert import pay_job_advert, publish_job_advert
from model.payment import store_payment


@api_token_required
def publish_advert_by_stripe_webhook_charge():
    request_content = request.json

    payment_id, job_id, advert_id = store_payment(request_content)
    pay_job_advert(job_id=job_id, advert_id=advert_id)
    publish_job_advert(job_id=job_id, advert_id=advert_id)

    return jsonify({'payment_id': payment_id})

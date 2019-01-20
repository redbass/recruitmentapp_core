
from flask import request
from flask_jwt_extended import get_jwt_identity

from api.handler import json_response
from auth.api_token import api_token_required
from integrations import stripe
from integrations.stripe import publish_payed_advert, pay_job_advert
from model.job.job import get_job


@api_token_required
@json_response
def charge_payment():
    data = request.json
    job_id = data.get('job_id', "")
    advert_id = data.get('advert_id', "")
    token = data.get('token', "")

    identity = get_jwt_identity()

    pay_job_advert(advert_id=advert_id, job_id=job_id, stripe_token=token,
                   user_id=identity['username'])
    job = get_job(job_id=job_id)
    return {'job': job}


@api_token_required
@json_response
def charge_processed():
    payment_id = publish_payed_advert(stripe_payload=request.json)
    return {'payment_id': payment_id}


@json_response
def get_stripe_config():
    conf = stripe.get_stripe_config()
    conf.pop('_id', None)
    return conf

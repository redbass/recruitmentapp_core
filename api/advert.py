from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model.job import job_advert


@jwt_required
@json_response
def create_advert(job_id: str):
    data = request.json

    duration = data.get('duration')

    try:
        duration = int(duration)
    except Exception:
        raise ValueError("'{duration}' is not an integer duration"
                         .format(duration=duration))

    return job_advert.create_advert_for_a_job(job_id=job_id,
                                              advert_duration=duration)


@jwt_required
@json_response
def approve_advert(job_id: str, advert_id: str):
    job_advert.approve_advert(job_id=job_id, advert_id=advert_id)

    return {
        'job_id': job_id,
        'advert_id': advert_id,
        'approved': True
    }

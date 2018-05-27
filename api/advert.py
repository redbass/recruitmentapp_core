from dateutil.parser import parse
from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model import job


@jwt_required
@json_response
def create_advert(job_id: str):
    data = request.json

    period = data.get('period', {})

    start = period.get('start')
    if start is None:
        raise ParametersException('Start period is required')

    end = period.get('end')

    try:
        start = parse(start)
        end = parse(end) if end else None
    except Exception:
        raise ValueError("Period dates have to be in ISO format")

    return job.create_advert_for_a_job(job_id=job_id,
                                       start_period=start,
                                       end_period=end)


@jwt_required
@json_response
def approve_advert(job_id: str, advert_id: str):

    job.approve_advert(job_id=job_id, advert_id=advert_id)

    return {
        'job_id': job_id,
        'advert_id': advert_id,
        'approved': True
    }

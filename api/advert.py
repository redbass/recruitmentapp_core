from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model.advert import AdvertStatus
from model.job import job_advert


map_action_to_status = {
    'publish': AdvertStatus.PUBLISHED,
    'approve': AdvertStatus.APPROVED,
}


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
def set_advert_status(job_id: str, advert_id: str, action: str):

    if action.lower() not in map_action_to_status:
        raise ValueError('Invalid action "{action}"'.format(action=action))

    new_status = map_action_to_status[action.lower()]
    job_advert.update_advert_status(
        job_id=job_id, advert_id=advert_id, new_status=new_status)

    return {
        'job_id': job_id,
        'advert_id': advert_id,
        'new_status': new_status
    }

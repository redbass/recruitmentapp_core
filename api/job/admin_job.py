from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from lib.schema_validation import validate
from model.job.create_job import create_job
from model.job.edit_job import edit_job
from model.job.job import get_job
from model.job.job_advert import approve_job_advert, publish_job_advert, \
    add_advert_to_job

map_advert_action = {
    'publish': publish_job_advert,
    'approve': approve_job_advert,
}


@jwt_required
@json_response
def api_create_job():
    data = request.json

    validate('create_job', data)

    return create_job(**data)


@jwt_required
@json_response
def api_edit_job(job_id):
    data = request.json

    validate('edit_job', data)

    return edit_job(_id=job_id, **data)


@jwt_required
@json_response
def api_add_advert_to_job(job_id: str):
    data = request.json
    duration = data.get('duration')

    return add_advert_to_job(job_id=job_id, advert_duration_days=duration)


@jwt_required
@json_response
def set_advert_status(job_id: str, advert_id: str, action: str):

    advert_action = map_advert_action.get(action.lower())
    if not advert_action:
        raise ValueError('Invalid action "{action}"'.format(action=action))

    advert_action(job_id=job_id, advert_id=advert_id)
    return get_job(job_id=job_id)

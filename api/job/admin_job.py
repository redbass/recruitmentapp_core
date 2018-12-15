from flask import request
from flask_jwt_extended import get_jwt_identity

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ActionNotAllowed
from lib.schema_validation import validate
from model.job.create_job import create_job
from model.job.edit_job import edit_job
from model.job.job import get_job
from model.job.job_advert import approve_job_advert, publish_job_advert, \
    add_advert_to_job, request_approval_job_advert, archive_job_advert
from model.job import AdvertStatus
from model.user import UserType


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
    identity = get_jwt_identity()
    job = get_job(job_id)

    if identity['role'] != UserType.ADMIN and \
            any(adv['status'] != AdvertStatus.DRAFT for adv in job['adverts']):
        raise ActionNotAllowed("User not allowed to edit an approved advert")

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

    map_advert_action = {
        'requestapproval': request_approval_job_advert,
        'approve': approve_job_advert,
        'publish': publish_job_advert,
        'archive': archive_job_advert
    }

    advert_action = map_advert_action.get(action.lower())
    if not advert_action:
        raise ValueError('Invalid action "{action}"'.format(action=action))

    advert_action(job_id=job_id, advert_id=advert_id)
    return get_job(job_id=job_id)

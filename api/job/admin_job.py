from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from lib.schema_validation import validate
from model.job.create_job import create_job
from model.job.edit_job import edit_job


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

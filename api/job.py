from flask import request
from flask_jwt_extended import jwt_required

from api.handler import json_response
from exceptions.api import ParametersException
from model import job


@jwt_required
@json_response
def get_job(_id: str):
    results = job.get_jobs([_id])
    return results[0] if results else []


@jwt_required
@json_response
def create_job():
    data = request.json
    if 'title' not in data or 'description' not in data:
        raise ParametersException("`title` and `description` arguments are mandatory")

    result = job.create_job(title=data['title'],
                            description=data['description'])
    return result

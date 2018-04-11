from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException, ArgumentException
from model import job


@jwt_required
@json_response
def get_job(_id: str = None):
    results = job.get_jobs([_id])
    return results[0] if results else []


@jwt_required
@json_response
def get_all_jobs():
    limit = _request_arg_to_str('limit') or 10
    start = _request_arg_to_str('start') or 0

    return job.get_all_jobs(limit, start)


@jwt_required
@json_response
def create_job():
    data = request.json
    if 'title' not in data or 'description' not in data:
        raise ParametersException("`title` and `description` arguments are mandatory")

    result = job.create_job(title=data['title'],
                            description=data['description'])
    return result


def _request_arg_to_str(arg_name: str):
    value = request.args.get(arg_name)
    try:
        if value:
            return int(value)
        return None

    except ValueError:
        raise ArgumentException("The input string '{s}' is not a valid number")
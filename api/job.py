from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model import NOT_PROVIDED
from model.job.create_job import create_job
from model.job.edit_job import edit_job
from model.job.job import get_jobs, get_job
from model.location import Location


@jwt_required
@json_response
def api_get_jobs():
    return get_jobs()


@jwt_required
@json_response
def api_get_job(job_id):
    return get_job(job_id=job_id)


@jwt_required
@json_response
def api_create_job():
    data = request.json
    company_id = data.get('company_id')
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')

    if not title or not description:
        raise ParametersException(
            '`title` and `description` arguments are mandatory')

    location = _validate_and_get_location(location)
    new_job = create_job(company_id=company_id, title=title,
                         description=description, location=location)
    return new_job


@jwt_required
@json_response
def api_edit_job(job_id):
    data = request.json
    title = data.get('title', NOT_PROVIDED)
    description = data.get('description', NOT_PROVIDED)
    location = data.get('location', NOT_PROVIDED)

    location = _validate_and_get_location(location)
    updated_job = edit_job(job_id=job_id, new_title=title,
                           new_description=description, new_location=location)
    return updated_job


def _validate_and_get_location(location):
    if location and location != NOT_PROVIDED:
        try:
            latitude = float(location.get('lat'))
            longitude = float(location.get('lng'))
        except TypeError:
            raise ValueError('Provided invalid location: {location}'
                             .format(location=location))

        return Location(latitude, longitude)
    return NOT_PROVIDED

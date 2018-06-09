from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model import job
from model.location import Location


@jwt_required
@json_response
def get_jobs():
    return job.get_jobs()


@jwt_required
@json_response
def create_job():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')

    if not title or not description:
        raise ParametersException(
            '`title` and `description` arguments are mandatory')

    if location:
        latitude = location.get('latitude')
        longitude = location.get('longitude')

        if not latitude or not longitude:
            raise ParametersException(
                'Location require a latitude and longitude')

        location = Location(latitude, longitude)

    return job.create_job(title, description, location)

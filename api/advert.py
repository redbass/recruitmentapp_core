from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException, ArgumentException
from model import advert
from model.location import Location


@jwt_required
@json_response
def get_advert(_id: str = None):
    results = advert.get_adverts([_id])
    return results[0] if results else []


@jwt_required
@json_response
def get_all_adverts():
    limit = _request_arg_to_str('limit') or 10
    start = _request_arg_to_str('start') or 0

    return advert.get_all_adverts(limit, start)


@jwt_required
@json_response
def create_adverts():
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

    return advert.create_advert(title, description, location)


def _request_arg_to_str(arg_name: str):
    value = request.args.get(arg_name)
    try:
        if value:
            return int(value)
        return None

    except ValueError:
        raise ArgumentException("The input string '{s}' is not a valid number")

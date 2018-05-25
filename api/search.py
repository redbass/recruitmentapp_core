import json

from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model.location import Location
from search import job


@jwt_required
@json_response
def search_adverts_by_radius():

    radius = _get_radius()
    location = _get_location()

    results = job.search_adverts_by_radius(location, radius)

    return results


def _get_radius():
    radius = request.args.get('radius')

    try:
        radius = json.loads(radius)
        radius = float(radius)

    except Exception:
        raise ParametersException("Invalid radius format")

    return radius


def _get_location():
    location = request.args.get('location')

    try:
        location = json.loads(location)

        if len(location) < 2 or 2 < len(location):
            raise Exception()

        location = Location(*location)

    except Exception:
        raise ParametersException("Invalid location format")

    return location

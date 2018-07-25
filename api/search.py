import json

from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model.location import Location
from search import jobs
from search.static_results import static_jobs


@jwt_required
@json_response
def search_adverts_by_radius():
    radius = _get_radius()
    location = _get_location()

    results = jobs.search_adverts_by_radius(location, radius)

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


@json_response
@api_token_required
def search():
    query = request.args.get('query', '')
    results = jobs.search(query)
    return {
        "jobs": results,
        "query": {
            "string": query
        }
    }


@json_response
@api_token_required
def search_static():

    query = ""

    return {
        "jobs": static_jobs,
        "query": {
            "string": query
        }
    }

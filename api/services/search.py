from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from auth.jwt import jwt_required
from exceptions.api import ParametersException
from model.geo_location import validate_lat_long_values
from search import jobs
from search.static_results import static_jobs


@jwt_required
@json_response
def search_adverts_by_radius():

    radius = _get_radius()
    coordinates = _get_coordinates()

    results = jobs.search_adverts_by_radius(coordinates, radius)

    return results


def _get_radius():
    radius = request.args.get('radius')

    try:
        radius = float(radius)

    except Exception:
        raise ParametersException("Invalid radius format")

    return radius


def _get_coordinates():
    location = request.args.get('location')

    try:
        coordinates = [float(c) for c in location.split(',')]

        if len(coordinates) != 2:
            raise Exception()

        validate_lat_long_values(*coordinates)

    except Exception:
        raise ParametersException("Invalid location format")

    return coordinates


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

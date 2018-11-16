from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from exceptions.api import ParametersException
from model.geo_location import validate_lat_long_values
from services.search import search


@json_response
@api_token_required
def api_search():
    query = request.args.get('query')

    location = _get_coordinates()
    distance = _get_distance()

    results = search(query=query, location=location, distance=distance)
    return {
        "jobs": results,
        "query": {
            "query": query,
            "location": location,
            "distance": distance
        }
    }


def _get_coordinates():
    location = request.args.get('location')

    if location:
        try:
            coordinates = [float(c) for c in location.split(',')]

            if len(coordinates) != 2:
                raise Exception()

            validate_lat_long_values(*coordinates)

        except Exception:
            raise ParametersException("Invalid location format")

        return coordinates
    return location


def _get_distance():
    distance = request.args.get('distance') or request.args.get('radius')

    if distance:
        try:
            distance = float(distance)

        except Exception:
            raise ParametersException("Invalid radius format")

    return distance

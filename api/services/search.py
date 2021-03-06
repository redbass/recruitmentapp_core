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
    job_type = request.args.get('job_type')
    rate_type = request.args.get('rate_type')

    page = request.args.get('page')
    page = int(page) if page else None

    limit = request.args.get('limit')
    limit = int(limit) if limit else None

    location = _get_coordinates()
    distance = _get_distance()

    results, total, pages = search(
        query=query, job_type=job_type, rate_type=rate_type, location=location,
        distance=distance, page=page, limit=limit
    )

    query = {
        'query': query,
        'job_type': job_type,
        'rate_type': rate_type,
        'location': location,
        'distance': distance,
        'page': page,
        'limit': limit
    }

    return {
        "jobs": results,
        "query": query,
        "total": total,
        "pages": pages
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

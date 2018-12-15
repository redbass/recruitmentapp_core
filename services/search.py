

from datetime import datetime

from db.collections import jobs
from lib.geo import km2rad
from model.job import AdvertStatus

DEFAULT_PAGE_SIZE = 10


def _prepare_results(result):
    results, count, pages = [], 0, 0

    result = list(result)

    if result:
        results = result[0]['result']
        count = result[0]['count']
        pages = int(result[0]['pages'])

    return results, count, pages


def search(query: str = "",
           location: list = None,
           distance: float = None,
           job_type: str = None,
           rate_type: str = None,
           page: int = None,
           limit: int = None):
    pipeline = []

    _add_match_query(pipeline=pipeline, query=query, job_type=job_type,
                     location=location, distance=distance, rate_type=rate_type)
    _add_lookup_query(pipeline)
    _add_order_by_advert_creation(pipeline)
    _add_computed_fields_query(pipeline)
    _add_pagination(pipeline, page, limit)

    result = jobs.aggregate(pipeline)

    return _prepare_results(result)


def _add_pagination(pipeline, page, limit):
    page = page or 0
    limit = limit or DEFAULT_PAGE_SIZE
    results_query = {'$slice': ['$result', page * limit, limit]}
    page_query = {'$ceil': {'$divide': [{'$size': '$result'}, limit]}}
    pipeline.extend([
        {
            '$group': {
                '_id': 'results', 'result': {'$push': '$$CURRENT'}}
        },
        {
            '$project': {
                '_id': 0,
                'count': {'$size': '$result'},
                'result': results_query,
                'pages': page_query},
        }
    ])


def _add_match_query(pipeline, query, job_type, rate_type, location, distance):
    today = datetime.combine(datetime.now(), datetime.min.time())
    match_queries = [
        {"adverts.date.expires": {"$gt": today}},
        {"adverts.status": AdvertStatus.PUBLISHED}
    ]

    if query:
        match_queries.append({"$text": {"$search": query}})

    if location and distance:
        rad_radius = km2rad(distance)
        latitude, longitude = location
        match_queries.append({
            "location.geo_location": {
                "$geoWithin": {
                    "$centerSphere": [[longitude, latitude], rad_radius]
                }}
        })

    if job_type:
        match_queries.append({"metadata.job_type": job_type})

    if rate_type:
        match_queries.append({"rate.type": rate_type})

    pipeline.append({"$match": {"$and": match_queries}})


def _add_order_by_advert_creation(pipeline):
    pipeline.extend([
        {"$addFields": {"advert": {"$arrayElemAt": ["$adverts", 0]}}},
        {"$project": {"adverts": 0}},
        {"$sort": {"advert.date.created": -1}}
    ])


def _add_lookup_query(pipeline):
    pipeline.extend([
        {
            "$lookup": {
                "from": "companies",
                "let": {
                    "c_id": "$company_id"
                },
                "pipeline": [{
                    "$match": {
                        "$expr": {
                            "$eq": ["$_id", "$$c_id"]}
                    }
                }],
                "as": "companies"
            }
        },
        {
            "$addFields": {
                "company": {"$arrayElemAt": ["$companies", 0]}}
        },
        {
            "$lookup": {
                "from": "users",
                "let": {
                    "hm_ids": "$company.hire_managers_ids"
                },
                "pipeline": [{
                    "$match": {
                        "$expr": {
                            "$in": ["$_id", "$$hm_ids"]}
                    }
                }],
                "as": "company.hiring_managers"
            }
        },
        {
            "$project": {
                "companies": 0,
                "company.hiring_managers.password": 0
            }}
    ])


def _add_computed_fields_query(pipeline):
    pipeline.append({
        "$addFields": {
            "rate.pretty_print": "100£ per day",
            "duration.pretty_print": "3 months and 2 weeks"
        }
    })

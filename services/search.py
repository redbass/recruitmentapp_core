from datetime import datetime

from db.collections import jobs
from lib.geo import km2rad
from model.job.job_advert import AdvertStatus


def search(query: str="",
           location: list=None,
           distance: float=None):

    pipeline = []

    _add_match_query(pipeline, query, location, distance)
    _add_lookup_query(pipeline)
    _add_computed_fields_query(pipeline)

    return jobs.aggregate(pipeline)


def _add_match_query(pipeline, query, location, distance):
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

    pipeline.append({"$match": {"$and": match_queries}})


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
        {"$addFields": {"company": {"$arrayElemAt": ["$companies", 0]}}},
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
        {"$project": {
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

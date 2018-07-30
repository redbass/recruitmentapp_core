from pymongo.cursor import Cursor

from db.collections import jobs
from model.location import Location


def search_adverts_by_radius(location: Location,
                             radius: float) -> Cursor:
    """
    Search all the Adverts in a circular area with the given `radius` and the
    center in `location`
    :param location: The center of the search area
    :param radius: The radius of the area in radians
    :return:
    """

    query = {
        "location": {
            "$geoWithin": {
                "$centerSphere": [
                    [location.longitude, location.latitude],
                    radius
                ]
            }
        }
    }

    return jobs.find(query)


def search(query: str):
    pipeline = [
        {"$match": {"$text": {"$search": query}}},

        {
            "$lookup": {
                "from": "companies",
                "let": {
                    "c_id": "$company_id"
                },
                "pipeline": [{
                    "$match": {
                        "$expr": {"$eq": ["$_id", "$$c_id"]}
                    }
                }],
                "as": "companies"
            }
        },

        {"$addFields": {"company": {"$arrayElemAt": ["$companies", 0]}}},

        {"$addFields": {"company": {"$arrayElemAt": ["$companies", 0]}}},

        {"$project": {"companies": 0}}
    ]

    return jobs.aggregate(pipeline)

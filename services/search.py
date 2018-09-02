from datetime import datetime

from db.collections import jobs


def search(query: str="",
           location: list=None,
           radius: float=None):
    today = datetime.combine(datetime.now(), datetime.min.time())

    match_queries = [{"adverts.date.expires": {"$gt": today}}]

    if query:
        match_queries.append({"$text": {"$search": query}})

    if location and radius:
        match_queries.append({
            "location.geo_location": {
                "$geoWithin": {"$centerSphere": [location, radius]}}
            })

    pipeline = [
        {
            "$match": {"$and": match_queries}
        },

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

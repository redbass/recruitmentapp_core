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

        {"$addFields": {
            "location.address": {
                "postcode": "$location.postcode",
                "address": "This is the address",
                "city": "Test Town",
            }
        }},

        {"$addFields": {"metadata.rate.pretty_print": "100£ per day"}},

        {"$addFields": {"metadata.company_referent.full_name": "John Doe"}},
        {"$addFields": {
            "metadata.company_referent.phone_number": "+44 7873590126"}},

        {"$addFields": {"duration.pretty_print": "3 months and 2 weeks"}},

        {"$addFields": {"company.logo": "http://findastart.palmerminto.com/"
                                        "wp-content/uploads/2018/06/"
                                        "cropped-Find-a-Start-logo@2x.png"}},

        {"$project": {"companies": 0}}
    ]

    return jobs.aggregate(pipeline)

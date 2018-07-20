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


@json_response
def search():
    return {
        "jobs": {
            "data": [
                {
                    "title": "Electrician",
                    "description": "summary text Lorem ipsum dolor sit amet, "
                                   "consectetur adipiscing elit. Aenean "
                                   "euismod bibendum laoreet. Proin gravi "
                                   "dolor sit amet lacus accumsa…",
                    "type": "Contract",
                    "duration": "6 weeks",
                    "location": "Bristol",
                    "company": [
                        {
                            "name": "Primoris Electrical",
                            "recruiting_contact": "Bob James",
                            "contact_phonenumber": "0773588632",
                            "logo": "/wp-content/uploads/2018/06/"
                                    "placeholder-image4.jpg"
                        }
                    ],
                    "rate": "£18 per hour",
                    "adverts": "xxx",
                    "skills": "xxx",
                    "qualifications": "xxx",
                    "advert": [
                        {
                            "_id": "1",
                            "date": [
                                {
                                    "published": "13/06/2018",
                                    "days_ago": "10"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Plumber",
                    "description": "summary text Lorem ipsum dolor sit amet, "
                                   "consectetur adipiscing elit. Aenean "
                                   "euismod bibendum laoreet. Proin gravi "
                                   "dolor sit amet lacus accumsa…",
                    "type": "Contract",
                    "duration": "4 months",
                    "location": "Bristol",
                    "company": [
                        {
                            "name": "Leaky Pete's Plumbing Services Ltd",
                            "recruiting_contact": "JJ Johnston",
                            "contact_phonenumber": "0773588632",
                            "logo": "/wp-content/uploads/2018/06/"
                                    "placeholder-image4.jpg"
                        }
                    ],
                    "rate": "£150 per day",
                    "adverts": "xxx",
                    "skills": "xxx",
                    "qualifications": "xxx",
                    "advert": [
                        {
                            "_id": "2",
                            "date": [
                                {
                                    "published": "13/06/2018",
                                    "days_ago": "2"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Plasterer",
                    "description": "summary text Lorem ipsum dolor sit amet, "
                                   "consectetur adipiscing elit. Aenean "
                                   "euismod bibendum laoreet. Proin gravi "
                                   "dolor sit amet lacus accumsa…",
                    "type": "Contract",
                    "duration": "2 months",
                    "location": "Bristol",
                    "company": [
                        {
                            "name": "Express Plastering Services Ltd",
                            "recruiting_contact": "Amanda Kiss",
                            "contact_phonenumber": "0773588632",
                            "logo": "/wp-content/uploads/2018/06/"
                                    "placeholder-image4.jpg"
                        }
                    ],
                    "rate": "£5 per square metre",
                    "adverts": "xxx",
                    "skills": "xxx",
                    "qualifications": "xxx",
                    "advert": [
                        {
                            "_id": "3",
                            "date": [
                                {
                                    "published": "14/06/2018",
                                    "days_ago": "13"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

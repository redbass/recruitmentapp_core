from db.collections import jobs
from model import create_id
from model.company.company import get_company
from model.geo_location import validate_lat_long_values, get_location


def create_job(company_id, location, **create_job_input):

    _validate_company_id(company_id)

    location = _input_location_to_location(location)

    create_job_input.update({
        "_id": create_id(),
        "company_id": company_id,
        "location": location
    })

    jobs.insert_one(create_job_input)
    return create_job_input


def _input_location_to_location(input_location):
    latitude = float(input_location.get('latitude'))
    longitude = float(input_location.get('longitude'))
    postcode = input_location.get('postcode')

    validate_lat_long_values(latitude, longitude)
    return get_location(postcode, latitude, longitude)


def _validate_company_id(company_id):
    if not get_company(company_id):
        raise ValueError('The company_id `{company_id}` is invalid'
                         .format(company_id=company_id))

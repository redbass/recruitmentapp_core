from datetime import datetime

from db.collections import jobs
from model import create_id
from model.company.company import get_company
from model.location import Location


def create_job(company_id: str,
               title: str,
               description: str,
               location: Location = None):

    if not all([title, description, company_id]):
        raise AttributeError('Title and Description are required',
                             company_id,
                             title,
                             description)

    if not get_company(company_id):
        raise ValueError('The company_id `{company_id}` is invalid'
                         .format(company_id=company_id))

    _id = create_id()
    job = {
        '_id': _id,
        'company_id': company_id,
        'title': title,
        'description': description,
        'location': location.get_geo_json_point() if location else None,
        'date': {
            'created': datetime.utcnow(),
            'updated': datetime.utcnow()
        }
    }
    jobs.insert_one(job)
    return job

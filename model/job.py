from db.collections import jobs
from model import create_id
from model.location import Location
from model.period import create_period


def create_job(title: str,
               description: str,
               location: Location = None):

    if not title or not description:
        raise AttributeError('Title and Description are required',
                             title,
                             description)

    _id = create_id()
    job = {
        '_id': _id,
        'title': title,
        'description': description,
        'period': create_period(),
        'location': location.get_geo_json_point() if location else None,
        'deleted': False
    }
    jobs.insert_one(job)
    return job


def delete_jobs(_ids: [str]):

    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    jobs.update_many({'_id': {'$in': _ids}},
                     {'$set': {'deleted': True}})


# def add_avert_to_job(job_id: str,
#                      advert: dict):
#     pass

from datetime import datetime

from db.collections import jobs
from model import create_id
from model.advert import create_advert
from model.location import Location
from model.period import create_period


def get_job(job_id: str):
    return jobs.find_one({'_id': job_id})


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


def create_advert_for_a_job(job_id: str,
                            start_period: datetime,
                            end_period: datetime):

    if not job_id:
        raise ValueError('job_id cannot be none')

    period = create_period(start=start_period, end=end_period)
    advert = create_advert(period)

    job = jobs.update_one({'_id': job_id},
                          {'$push': {'adverts': advert}})

    if job.matched_count == 0:
        raise ValueError('The job with id `{job_id}` has not been found'
                         .format(job_id=job_id))

    return job.raw_result

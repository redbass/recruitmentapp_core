from db.collections import jobs

from model import create_id
from model.period import create_period


def create_job(title: str,
               description: str) -> dict:

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
        'draft': False,
        'deleted': False
    }
    jobs.insert_one(job)
    return job


def delete_jobs(_ids: [str]):

    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be an list of ids')

    jobs.update_many({'_id': {'$in': _ids}},
                     {'$set': {'deleted': True}})

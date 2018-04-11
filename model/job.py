from pymongo.cursor import Cursor

from db.collections import jobs
from lib.pagination import get_pagination_from_cursor
from model import create_id
from model.period import create_period


DEFAULT_JOBS_PAGINATION_START = 0
DEFAULT_JOBS_PAGINATION_LIMIT = 10


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
        raise AttributeError('_ids have to be a list of ids')

    jobs.update_many({'_id': {'$in': _ids}},
                     {'$set': {'deleted': True}})


def get_jobs(_ids: [str]) -> [Cursor]:
    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    return [job for job in jobs.find({'_id': {'$in': _ids}})]


def get_all_jobs(limit: int, start: int):
    limit = limit or DEFAULT_JOBS_PAGINATION_LIMIT
    start = start or DEFAULT_JOBS_PAGINATION_START

    cursor = jobs.find({})
    return get_pagination_from_cursor(cursor, start, limit)

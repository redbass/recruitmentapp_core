from pymongo.cursor import Cursor

from db.collections import adverts
from lib.pagination import get_pagination_from_cursor
from model import create_id
from model.location import Location
from model.period import create_period


DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


def create_advert(title: str,
                  description: str,
                  location: Location=None) -> dict:

    if not title or not description:
        raise AttributeError('Title and Description are required',
                             title,
                             description)

    _id = create_id()
    advert = {
        '_id': _id,
        'title': title,
        'description': description,
        'period': create_period(),
        'location': location.get_geo_json_point() if location else None,
        'draft': False,
        'deleted': False
    }
    adverts.insert_one(advert)
    return advert


def delete_adverts(_ids: [str]):

    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    adverts.update_many({'_id': {'$in': _ids}},
                        {'$set': {'deleted': True}})


def get_adverts(_ids: [str]) -> [Cursor]:
    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    return [advert for advert in adverts.find({'_id': {'$in': _ids}})]


def get_all_adverts(limit: int, start: int):
    limit = limit or DEFAULT_ADVERTS_PAGINATION_LIMIT
    start = start or DEFAULT_ADVERTS_PAGINATION_START

    cursor = adverts.find({})
    return get_pagination_from_cursor(cursor, start, limit)

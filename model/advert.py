from datetime import datetime

from model import create_id

DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


class AdvertStatus:
    DRAFT = 'DRAFT'
    APPROVED = 'APPROVED'


def create_advert(duration: int) -> dict:
    if not duration or duration < 0:
        raise ValueError(
            '{d} is not a valid duration period'.format(d=duration))

    _id = create_id()
    advert = {
        '_id': _id,
        'status': AdvertStatus.DRAFT,
        'duration': duration,
        'deleted': False
    }
    update_object_modification_date(advert)
    return advert


def update_object_modification_date(dict):
    if 'date' not in dict:
        dict['date'] = {
            'created': datetime.utcnow(),
        }

    dict['date']['updated'] = datetime.utcnow()

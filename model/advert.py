from datetime import datetime

from model import create_id

DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


class AdvertStatus:
    DRAFT = 'DRAFT'
    APPROVED = 'APPROVED'


def create_advert(publication_date: datetime) -> dict:
    if not publication_date:
        raise ValueError(
            "An advert have to be created with a publication date")

    _id = create_id()
    advert = {
        '_id': _id,
        'status': AdvertStatus.DRAFT,
        'date': {
            'created': datetime.utcnow(),
            'updated': datetime.utcnow(),
            'published': publication_date,
            'expire': None
        },
        'deleted': False
    }

    return advert

from datetime import datetime
from enum import Enum

from model import create_id

DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


class AdvertStatus(Enum):
    DRAFT = 'DRAFT'
    APPROVED = 'APPROVED'

    def __eq__(self, o: object) -> bool:

        if type(o) == str:
            return self.value == o

        return super().__eq__(o)


def create_advert(publication_date: datetime) -> dict:
    if not publication_date:
        raise ValueError(
            "An advert have to be created with a publication date")

    _id = create_id()
    advert = {
        '_id': _id,
        'status': AdvertStatus.DRAFT.value,
        'date': {
            'created': datetime.utcnow(),
            'updated': datetime.utcnow(),
            'published': publication_date,
            'expire': None
        },
        'deleted': False
    }

    return advert

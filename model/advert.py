from datetime import datetime
from enum import Enum

from model import create_id
from model.period import validate_period

DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


class AdvertStatus(Enum):
    DRAFT = 'DRAFT'
    APPROVED = 'APPROVED'

    def __eq__(self, o: object) -> bool:

        if type(o) == str:
            return self.value == o

        return super().__eq__(o)


def create_advert(period: dict) -> dict:

    validate_period(period)

    _id = create_id()
    advert = {
        '_id': _id,
        'status': AdvertStatus.DRAFT.value,
        'period': period,
        'date': {
            'created': datetime.utcnow(),
            'expire': None
        },
        'deleted': False
    }

    return advert

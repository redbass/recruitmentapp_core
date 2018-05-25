from datetime import datetime
from enum import Enum

from model import create_id
from model.job import add_avert_to_job

DEFAULT_ADVERTS_PAGINATION_START = 0
DEFAULT_ADVERTS_PAGINATION_LIMIT = 10


class AdvertStatus(Enum):
    DRAFT = 'DRAFT'
    APPROVED = 'APPROVED'

    def __eq__(self, o: object) -> bool:

        if type(o) == str:
            return self.value == o

        return super().__eq__(o)


def create_advert(job_id: str) -> dict:

    _id = create_id()
    advert = {
        '_id': _id,
        'status': AdvertStatus.DRAFT.value,
        'date': {
            'created': datetime.utcnow(),
            'expire': None
        },
        'deleted': False
    }
    job = add_avert_to_job(job_id, advert)

    if not job.get('updatedExisting'):
        raise AttributeError("The given 'job_id' doesnt match any stored job.")

    return advert

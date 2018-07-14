from datetime import datetime

from db.collections import jobs
from exceptions.model import GenericError
from model.advert import create_advert, AdvertStatus
from model.period import create_period


def create_advert_for_a_job(job_id: str,
                            start_period: datetime,
                            end_period: datetime = None):
    if not job_id:
        raise ValueError('job_id cannot be none')

    period = create_period(start=start_period, end=end_period)
    advert = create_advert(period)

    job = jobs.update_one(
        {'_id': job_id},
        {
            '$push': {'adverts': advert},
            '$set': {'date.updated': datetime.utcnow()}
        })

    if job.matched_count == 0:
        raise ValueError('The job with id `{job_id}` has not been found'
                         .format(job_id=job_id))

    return advert


def approve_advert(job_id: str, advert_id: str):
    job = jobs.find_one(
        {'_id': job_id, 'adverts._id': advert_id, 'adverts.status': 'DRAFT'}
    )

    if not job:
        raise ValueError('The advert is not in `DRAFT` or does not exists:'
                         '(job: `{job_id}`, advert: `{advert_id}'
                         .format(job_id=job_id, advert_id=advert_id))

    result = jobs.update_one(
        {'_id': job_id, 'adverts._id': advert_id},
        {'$set': {'adverts.$.status': AdvertStatus.APPROVED}}
    )

    if result.modified_count == 0:
        raise GenericError(
            'The advert with id `{advert_id}` has not been updated'
            .format(advert_id=advert_id))

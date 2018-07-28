from datetime import datetime

from db.collections import jobs
from model.advert import create_advert


def create_advert_for_a_job(job_id: str,
                            advert_duration: int):
    if not job_id:
        raise ValueError('job_id cannot be none')

    advert = create_advert(duration=advert_duration)

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


def update_advert_status(advert_id, job_id, new_status):
    job = jobs.find_one(
        {
            '_id': job_id,
            'adverts._id': advert_id,
            'adverts.status': 'DRAFT'
        }
    )
    if not job:
        raise ValueError('The advert is not in `DRAFT` or does not exists:'
                         '(job: `{job_id}`, advert: `{advert_id}`)'
                         .format(job_id=job_id, advert_id=advert_id))

    updated_date = datetime.utcnow()
    new_status_log = {
        'status': new_status,
        'date': updated_date
    }

    jobs.update_one(
        {
            '_id': job_id,
            'adverts._id': advert_id},
        {
            '$set': {
                'date.updated': updated_date,
                'adverts.$.status': new_status,
                'adverts.$.date.' + new_status.lower(): updated_date,
                'adverts.$.date.updated': updated_date
            },
            '$addToSet': {
                'adverts.$.status_log': new_status_log
            }
        }
    )

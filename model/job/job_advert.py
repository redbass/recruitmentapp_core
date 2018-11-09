from datetime import datetime, timedelta

from db.collections import jobs
from model import create_id
from model.job.job import get_job


class AdvertStatus:
    DRAFT = 'DRAFT'
    REQUEST_APPROVAL = 'REQUEST_APPROVAL'
    APPROVED = 'APPROVED'
    PAYED = 'PAYED'
    PUBLISHED = 'PUBLISHED'


def add_advert_to_job(job_id: str,
                      advert_duration_days: int):
    advert = _create_advert_dict(duration=advert_duration_days)

    job = jobs.update_one(
        {
            '_id': job_id},
        {
            '$push': {
                'adverts': advert},
            '$set': {
                'date.updated': datetime.utcnow()}
        })

    if job.matched_count == 0:
        raise ValueError('The job with id `{job_id}` has not been found'
                         .format(job_id=job_id))

    return advert


def request_approval_job_advert(advert_id, job_id):
    return _update_advert_status(
        advert_id=advert_id, job_id=job_id,
        allowed_statuses=[AdvertStatus.DRAFT],
        new_status=AdvertStatus.REQUEST_APPROVAL)


def approve_job_advert(advert_id, job_id):
    return _update_advert_status(
        advert_id=advert_id, job_id=job_id,
        allowed_statuses=[AdvertStatus.DRAFT,
                          AdvertStatus.REQUEST_APPROVAL],
        new_status=AdvertStatus.APPROVED)


def pay_job_advert(advert_id, job_id):
    return _update_advert_status(
        advert_id=advert_id, job_id=job_id,
        allowed_statuses=[AdvertStatus.APPROVED],
        new_status=AdvertStatus.PAYED)


def publish_payed_job_advert(advert_id, job_id):
    return _update_advert_status(
        advert_id=advert_id, job_id=job_id,
        allowed_statuses=[AdvertStatus.PAYED],
        new_status=AdvertStatus.PUBLISHED)


def publish_job_advert(advert_id, job_id):
    return _update_advert_status(
        advert_id=advert_id, job_id=job_id,
        allowed_statuses=[AdvertStatus.APPROVED,
                          AdvertStatus.PAYED],
        new_status=AdvertStatus.PUBLISHED)


def _create_advert_dict(duration: int) -> dict:
    if not duration or not isinstance(duration, int) or duration < 0:
        raise ValueError(
            "'{d}' is not a valid duration".format(d=duration))

    _id = create_id()
    return {
        '_id': _id,
        'status': AdvertStatus.DRAFT,
        'duration': duration,
        'date': {
            'created': datetime.utcnow(),
            'updated': datetime.utcnow()
        }
    }


def _update_advert_status(advert_id, job_id, allowed_statuses, new_status):
    updated_date = datetime.utcnow()

    new_values = {
        'adverts.$.status': new_status,
        'adverts.$.date.updated': updated_date,
        'adverts.$.date.' + new_status.lower(): updated_date,
    }

    if new_status == AdvertStatus.PUBLISHED:
        job = get_job(job_id)
        if job and 'adverts' in job and job.get('adverts'):
            duration = job['adverts'][0]['duration']
            expire_date = datetime.now() + timedelta(days=duration)
            new_values['adverts.$.date.expires'] = expire_date

    job = jobs.update_one(
        {
            '_id': job_id,
            'adverts': {
                '$elemMatch': {
                    'status': {
                        "$in": allowed_statuses},
                    '_id': advert_id,
                }
            }
        },
        {
            '$set': new_values,
            '$addToSet': {
                'adverts.$.status_log': {
                    'status': new_status,
                    'date': updated_date
                }
            }
        }
    )

    if job.matched_count == 0:
        raise ValueError('Impossible to update the advert status to {status}'
                         .format(status=new_status))

    return job

from datetime import datetime

from db.collections import jobs


def get_jobs():
    return jobs.find({})


def get_job(job_id: str):
    job = jobs.find_one({'_id': job_id})

    if not job:
        raise ValueError("Impossible to find the job '{job_id}"
                         .format(job_id=job_id))
    return job


def delete_jobs(_ids: [str]):
    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    jobs.update_many({'_id': {'$in': _ids}},
                     {'$set': {
                         'deleted': True,
                         'date.updated': datetime.utcnow()}})

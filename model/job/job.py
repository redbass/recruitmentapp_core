from datetime import datetime

from db.collections import jobs
from model.job import AdvertStatus


def get_jobs(company_id=None,
             adverts_status_filter=None,
             exclude_draft=False):
    pipeline = [
        {
            "$lookup": {
                "from": "companies",
                "let": {
                    "c_id": "$company_id"
                },
                "pipeline": [{
                    "$match": {
                        "$expr": {"$eq": ["$_id", "$$c_id"]}
                    }
                }],
                "as": "companies"
            }
        },
        {"$addFields": {"company": {"$arrayElemAt": ["$companies", 0]}}},
        {"$addFields": {"company_name": "$company.name"}},
        {"$project": {"companies": 0, "company": 0}}
    ]

    if company_id:
        pipeline.insert(0, {"$match": {"company_id": company_id}})

    if adverts_status_filter:
        match = {"$match": {"adverts.status": adverts_status_filter}}
        pipeline.insert(0, match)

    if exclude_draft:
        match = {"$match": {"adverts.status": {"$ne": AdvertStatus.DRAFT}}}
        pipeline.insert(0, match)

    results = jobs.aggregate(pipeline)

    return results


def get_job(job_id: str):
    job = jobs.find_one({'_id': job_id})

    if not job:
        raise ValueError("Job id '{job_id}' invalid or not found"
                         .format(job_id=job_id))
    return job


def delete_jobs(_ids: [str]):
    if not _ids or not isinstance(_ids, list):
        raise AttributeError('_ids have to be a list of ids')

    jobs.update_many({'_id': {'$in': _ids}},
                     {'$set': {
                         'deleted': True,
                         'date.updated': datetime.utcnow()}})

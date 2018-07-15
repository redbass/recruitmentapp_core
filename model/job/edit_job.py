from db.collections import jobs
from model import NOT_PROVIDED
from model.job.job import get_job
from model.location import Location


def edit_job(job_id: str,
             new_title: str = NOT_PROVIDED,
             new_description: str = NOT_PROVIDED,
             new_location: Location = NOT_PROVIDED):

    get_job(job_id)

    update_query = {}

    if new_title != NOT_PROVIDED:
        update_query['title'] = new_title

    if new_description != NOT_PROVIDED:
        update_query['description'] = new_description

    if new_location != NOT_PROVIDED:
        update_query['location'] = new_location.get_geo_json_point() \
            if new_location else None

    jobs.update({'_id': job_id},
                {'$set': update_query})

    return get_job(job_id)

from db.collections import jobs
from db.utils import dict_to_datapath
from model.job.create_job import _input_location_to_location
from model.job.job import get_job


def edit_job(_id: str,
             location=None,
             **new_values):

    if 'company_id' in new_values:
        raise ValueError("Job's company cannot be modified")

    if not get_job(_id):
        raise ValueError('Job id "{job_id}" does not exists'
                         .format(job_id=_id))

    if location:
        new_values['location'] = _input_location_to_location(location)

    exploded_values = dict_to_datapath(new_values)

    jobs.update({"_id": _id},
                {"$set": exploded_values})

    return get_job(_id)

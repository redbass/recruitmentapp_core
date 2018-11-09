from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model.job.job import get_jobs, get_job


@jwt_required
@json_response
def api_get_jobs():
    adverts_status_filter = request.args.get('advertsStatusFilter', None)
    return get_jobs(adverts_status_filter=adverts_status_filter)


@jwt_required
@json_response
def api_get_job(job_id):
    return get_job(job_id=job_id)

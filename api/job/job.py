from api.handler import json_response
from auth.jwt import jwt_required
from model.job.job import get_jobs, get_job


@jwt_required
@json_response
def api_get_jobs():
    return get_jobs()


@jwt_required
@json_response
def api_get_job(job_id):
    return get_job(job_id=job_id)

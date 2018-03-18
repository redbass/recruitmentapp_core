from api.handler import json_response
from model import job


@json_response
def get_job(_id: str):
    results = job.get_jobs([_id])
    return results[0] if results else []

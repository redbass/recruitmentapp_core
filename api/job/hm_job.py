from flask_jwt_extended import get_jwt_identity

from api.handler import json_response
from auth.jwt import jwt_required
from model.company.company import get_company_by_admin_user
from model.job.job import get_jobs


@jwt_required
@json_response
def api_get_company_jobs():
    identity = get_jwt_identity()
    company = get_company_by_admin_user(identity['username'])
    return get_jobs(company.get('_id', ''))

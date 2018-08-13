from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from lib.schema_validation import validate
from model import user
from model.company import company
from model.company import edit_company as edit_company_model


@jwt_required
@json_response
def create_company():
    data = request.json

    validate('create_company', data)

    # TODO: Replace with: `company_user = get_jwt_identity()`
    company_user = user.get_user('super_user')

    return company.create_company(admin_user_ids=[company_user['_id']], **data)


@jwt_required
@json_response
def edit_company(company_id):
    data = request.json

    return edit_company_model.edit_company(_id=company_id, **data)


@jwt_required
@json_response
def get_companies():
    return company.get_companies()


@jwt_required
@json_response
def get_company(company_id):
    return company.get_company(company_id=company_id)

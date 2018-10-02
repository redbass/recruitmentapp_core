from flask import request
from flask_jwt_extended import get_jwt_identity

from api.handler import json_response
from auth.jwt import jwt_required
from lib.schema_validation import validate
from model.company import company
from model.company import edit_company as edit_company_model


@jwt_required
@json_response
def create_company():
    identity = get_jwt_identity()
    data = request.json

    validate('create_company', data)

    return company.create_company(
        admin_user_ids=[identity['username']], **data)


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

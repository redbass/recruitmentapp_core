from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model import user, NOT_PROVIDED
from model.company import company
from model.company import edit_company as edit_company_model


@jwt_required
@json_response
def create_company():
    data = request.json

    name = data.get('name')
    description = data.get('description')

    # TODO: Replace with: `company_user = get_jwt_identity()`
    company_user = user.get_user('super_user')

    return company.create_company(name=name,
                                  description=description,
                                  admin_user_id=company_user['_id'])


@jwt_required
@json_response
def edit_company(company_id):
    data = request.json

    new_name = data.get('name', NOT_PROVIDED)
    new_description = data.get('description', NOT_PROVIDED)

    return edit_company_model.edit_company(company_id=company_id,
                                           new_name=new_name,
                                           new_description=new_description)


@jwt_required
@json_response
def get_companies():
    return company.get_companies()


@jwt_required
@json_response
def get_company(company_id):
    return company.get_company(company_id=company_id)

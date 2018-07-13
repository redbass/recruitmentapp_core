from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model import user
from model.company import company
from model.user import UserType


@jwt_required
@json_response
def create_company():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    company_user = user.create_user(username=username,
                                    email=email,
                                    password=password,
                                    user_type=UserType.HIRING_MANAGER)

    return _create_company(company_user, data)


@jwt_required
@json_response
def admin_create_company():
    data = request.json

    # TODO: Replace with: `company_user = get_jwt_identity()`
    company_user = user.get_user('super_user')

    return _create_company(company_user, data)


def _create_company(company_user, data):
    name = data.get('name')
    description = data.get('description')
    return company.create_company(name=name,
                                  description=description,
                                  admin_user_id=company_user['_id'])


@jwt_required
@json_response
def get_companies():
    return company.get_companies()


@jwt_required
@json_response
def get_company(company_id):
    return company.get_company(company_id=company_id)

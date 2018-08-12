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

    name = data.get('name')
    description = data.get('description')

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    company_user = user.create_user(username=username,
                                    email=email,
                                    password=password,
                                    user_type=UserType.HIRING_MANAGER)

    return company.create_company(name=name,
                                  description=description,
                                  admin_user_ids=[company_user['_id']])

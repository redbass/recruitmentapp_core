from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from lib.schema_validation import validate
from model import user
from model.company import company
from model.company.company import get_company
from model.user import UserType


@api_token_required
@json_response
def sign_in_company():
    data = request.json

    validate('sign_in_company', data)

    data = request.json

    hm_data = {
        "username": data.get('hm_email'),
        "password": data.get('hm_password'),
        "first_name": data.get('hm_first_name'),
        "last_name": data.get('hm_last_name'),
        "title": data.get('hm_title')
    }

    company_user = user.create_user(user_type=UserType.HIRING_MANAGER,
                                    **hm_data)

    company_data = {
        "name": data.get('company_name'),
        "description": data.get('company_description')
    }

    created_company = company.create_company_hiring_manager(
        admin_user_id=company_user['_id'], **company_data)

    return get_company(created_company['_id'])

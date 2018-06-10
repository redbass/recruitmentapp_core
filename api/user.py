from flask import request

from api.handler import json_response
from model import user
from model.user import UserType


@json_response
def create_user():
    data = request.json

    email = data.get('email', '')
    password = data.get('password', '')
    user_type = getattr(UserType, data.get('user_type', ''),
                        UserType.CANDIDATE)

    user.create_user(email=email, password=password, user_type=user_type)

    return {}

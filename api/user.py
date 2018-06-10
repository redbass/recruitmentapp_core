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


@json_response
def get_users(user_type: str = None):

    if not hasattr(UserType, user_type.upper()):
        raise ValueError('Invalid user_type `{user_type}`'
                         .format(user_type=user_type))

    users = user.get_users(user_type=user_type)
    return users

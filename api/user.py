from flask import request

from api.handler import json_response
from auth.jwt import jwt_required
from model import user
from model.user import UserType, get_user as get_user_model


@jwt_required
@json_response
def get_users():

    user_type = request.args.get('type')
    if user_type:
        user_type = user_type.upper()
        if not hasattr(UserType, user_type):
            raise ValueError('Invalid user_type `{user_type}`'
                             .format(user_type=user_type))

    users = user.get_users(user_type=user_type, exclude_password=True)
    return users


@jwt_required
@json_response
def get_user(user_id):
    return get_user_model(username=user_id, exclude_password=True)

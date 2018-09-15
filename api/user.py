from api.handler import json_response
from auth.jwt import jwt_required
from model import user
from model.user import UserType


@jwt_required()
@json_response
def get_users(user_type: str = None):

    user_type = user_type.upper()
    if not hasattr(UserType, user_type):
        raise ValueError('Invalid user_type `{user_type}`'
                         .format(user_type=user_type))

    users = user.get_users(user_type=user_type)
    return users

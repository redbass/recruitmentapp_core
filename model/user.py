from db.collections import users
from lib.validation import validate_email


class UserType:
    ADMIN = 'A'
    HIRING_MANAGER = 'HM'
    CANDIDATE = 'C'


def create_user(email: str, password: str,
                user_type: UserType = UserType.CANDIDATE):

    if not email or not password:
        raise ValueError('Email and password are both required')

    if not validate_email(email=email):
        raise ValueError('Invalid email')

    return users.insert_one({'_id': email,
                             'password': password,
                             'type': user_type})

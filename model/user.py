from db.collections import users
from lib.password import encrypt_password
from lib.validation import validate_email


class UserType:
    ADMIN = 'ADMIN'
    HIRING_MANAGER = 'HIRING_MANAGER'
    CANDIDATE = 'CANDIDATE'


def create_user(username: str,
                email: str,
                password: str,
                user_type: UserType = UserType.CANDIDATE):

    if not all([username, email, password]):
        raise ValueError('Username, email, password are all required')

    if not validate_email(email=email):
        raise ValueError('Invalid email')

    duplicate = users.find_one({'$or': [
        {'_id': username},
        {'email': email}
    ]})

    if duplicate and duplicate['_id']:
        raise ValueError('Username `{username}` has already been used'
                         .format(username=username))

    if duplicate and duplicate['email']:
        raise ValueError('Email `{email}` has already been used'
                         .format(email=email))

    new_user = {
        '_id': username,
        'email': email,
        'password': encrypt_password(password),
        'type': user_type}
    users.insert_one(new_user)

    return new_user


def get_users(user_type: str):
    return users.find({'type': user_type},
                      {'_id': 1, 'email': 1, 'type': 1})


def get_user(username: str):
    return users.find_one({'_id': username})

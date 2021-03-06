from uuid import uuid4

from pymongo.errors import DuplicateKeyError

from db.collections import users
from lib.password import encrypt_user_password
from lib.validation import validate_email


class UserType:
    ADMIN = 'ADMIN'
    HIRING_MANAGER = 'HIRING_MANAGER'
    CANDIDATE = 'CANDIDATE'


def create_user(username: str,
                password: str,
                first_name: str,
                last_name: str,
                user_type: str = UserType.CANDIDATE,
                title: str = None,
                **_):

    if not validate_email(email=username):
        raise ValueError('Invalid username (not a valid email)')

    new_user = {
        '_id': username,
        'password': encrypt_user_password(password),
        'type': user_type,
        'first_name': first_name,
        'last_name': last_name,
        'title': title
    }

    try:
        users.insert_one(new_user)
    except DuplicateKeyError:
        raise ValueError("A user with this email already exists")

    return new_user


def create_hidden_hiring_manager(username: str):
    password = uuid4().hex
    return create_user(username=username,
                       password=password,
                       user_type=UserType.HIRING_MANAGER,
                       first_name=username,
                       last_name=username)


def get_users(user_type=None, exclude_password=False):
    return _query_users_filtering_password(
        find_fn=users.find,
        query={'type': user_type} if user_type else {},
        exclude_password=exclude_password)


def get_user(username: str, exclude_password=False):
    return _query_users_filtering_password(
        find_fn=users.find_one,
        query={'_id': username},
        exclude_password=exclude_password)


def update_user_password(user_id, new_password):

    encoded_password = encrypt_user_password(new_password)

    result = users.update_one({'_id': user_id},
                              {'$set': {'password': encoded_password}})

    if result.matched_count != 1:
        raise ValueError("Invalid user id")


def _query_users_filtering_password(find_fn, query, exclude_password=True):
    args = [query]
    if exclude_password:
        args.append({'password': 0})

    return find_fn(*args)

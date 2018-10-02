from typing import List

from db.collections import companies, users
from model import create_id
from model.user import UserType


def create_company(admin_user_ids: List[str],
                   **create_company_input):

    _validate_admin_ids(admin_user_ids)

    create_company_input.update({
        '_id': create_id(),
        'hire_managers_ids': admin_user_ids,
        'admin_user_ids': admin_user_ids,
    })
    companies.insert_one(create_company_input)
    return create_company_input


def _validate_admin_ids(admin_user_ids):
    for _id in admin_user_ids:
        _validate_admin_id(_id)


def _validate_admin_id(admin_user_id):
    admin_user = users.find_one({
                                    '_id': admin_user_id})
    if not admin_user:
        raise ValueError("The given user admin id `{_id}` is not valid"
                         .format(_id=admin_user_id))
    if admin_user['type'] not in [UserType.HIRING_MANAGER, UserType.ADMIN]:
        raise ValueError("The given user admin id `{_id}` is not a "
                         "`hiring manager` or an `admin`"
                         .format(_id=admin_user_id))
    if admin_user['type'] == UserType.HIRING_MANAGER and \
            get_company_by_admin_user(admin_user_id=admin_user_id):
        raise ValueError("A company with the same admin user `{_id}` already "
                         "exists".format(_id=admin_user_id))


def get_company(company_id: str):
    return companies.find_one({'_id': company_id})


def get_companies(ids: list=None):
    query = {} if not ids else {'_id': {'$in': ids}}
    return companies.find(query)


def get_company_by_admin_user(admin_user_id: str):
    return companies.find_one({'admin_user_ids': admin_user_id})

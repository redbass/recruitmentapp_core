from db.collections import companies, users
from model import create_id
from model.user import UserType


def create_company(name: str,
                   admin_user_id: str,
                   description: str = None):
    if not name:
        raise ValueError("Company `name` is a required field")

    admin_user = users.find_one({'_id': admin_user_id})

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

    company = {
        "_id": create_id(),
        "name": name,
        "description": description,
        "admin_user_ids": [admin_user_id],
        "hire_managers_ids": []
    }
    companies.insert_one(company)
    return company


def get_company(company_id: str):
    return companies.find_one({'_id': company_id})


def get_companies(ids: list=None):
    query = {} if not ids else {'_id': {'$in': ids}}
    return companies.find(query)


def get_company_by_admin_user(admin_user_id: str):
    return companies.find_one({'admin_user_ids': admin_user_id})

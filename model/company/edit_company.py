from db.collections import companies
from model import NOT_PROVIDED
from model.company.company import get_company


def edit_company(company_id: str,
                 new_name: str = NOT_PROVIDED,
                 new_description: str = NOT_PROVIDED):

    new_values = {}

    if None in [new_name, new_description]:
        raise ValueError('Company name and description cannot be null '
                         'or empty string')

    if "" in [new_name, new_description]:
        raise ValueError('Company name and description cannot be null '
                         'or empty string')

    if new_name and new_name != NOT_PROVIDED:
        new_values['name'] = new_name

    if new_description and new_description != NOT_PROVIDED:
        new_values['description'] = new_description

    if not companies.find_one({"_id": company_id}):
        raise ValueError('Company id "{company_id}" does not exists'
                         .format(company_id=company_id))

    companies.update({"_id": company_id},
                     {"$set": new_values})

    return get_company(company_id)

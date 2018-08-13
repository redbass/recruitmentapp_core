from db.collections import companies
from db.utils import dict_to_datapath
from model.company.company import get_company


def edit_company(_id: str,
                 **new_values):

    if not companies.find_one({"_id": _id}):
        raise ValueError('Company id "{company_id}" does not exists'
                         .format(company_id=_id))

    exploded_values = dict_to_datapath(new_values)

    companies.update({"_id": _id},
                     {"$set": exploded_values})

    return get_company(_id)

from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from model.picklist import get_picklist as model_get_picklist, \
    store_piclikst as model_store_piclikst


@json_response
@api_token_required
def get_picklist(name):
    return model_get_picklist(picklist_type=name)


@json_response
@api_token_required
def store_picklist(name):
    model_store_piclikst(picklist_type=name, picklist_values=request.json)

    return {}

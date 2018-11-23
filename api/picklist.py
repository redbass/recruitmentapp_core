from api.handler import json_response
from auth.api_token import api_token_required
from model.picklist import get_picklist


@json_response
@api_token_required
def picklist(name):
    return get_picklist(name)

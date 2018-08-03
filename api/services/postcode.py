from api.handler import json_response
from auth.api_token import api_token_required
from services.postcode import get_postcode as lib_get_postcode


@api_token_required
@json_response
def get_postcode(postcode):

    postcode_data = lib_get_postcode(postcode)

    return postcode_data.get('result', {})

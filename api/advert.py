from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from lib.schema_validation import validate
from model.job.application import apply_advert


@api_token_required
@json_response
def api_apply_advert(advert_id):
    candidate = request.json

    validate('advert_application', candidate)
    apply_advert(advert_id, **candidate)

    return {'submitted': True}

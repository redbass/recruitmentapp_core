
from flask import request

from api.handler import json_response
from auth.api_token import api_token_required
from integrations.stripe import publish_payed_advert


@api_token_required
@json_response
def stripe_charge_processed():
    payment_id = publish_payed_advert(request.json)
    return {'payment_id': payment_id}

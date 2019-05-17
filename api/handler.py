from functools import wraps

from flask.json import jsonify
from jsonschema import ValidationError
from jwt import ExpiredSignatureError

from exceptions.api import ParametersException, ActionNotAllowed
from exceptions.auth import UnauthorizedException
from exceptions.integrations import StripeException, SendgridException
from exceptions.service import ServiceError

EXCEPTIONS = {
    ParametersException: 400,
    ValueError: 400,
    ValidationError: 400,
    ActionNotAllowed: 400,
    ExpiredSignatureError: 401,
    UnauthorizedException: 405,
    ServiceError: 503,
    StripeException: 500,
    SendgridException: 500
}


def json_response(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            result = f(*args, **kwargs)
            return jsonify(result), 200

        except Exception as e:
            return _error_handler(e)

    return wrapper


def _error_handler(e):

    e_msg = str(e)
    code = 500

    if type(e) in EXCEPTIONS:
        code = EXCEPTIONS[type(e)]

    if isinstance(e, ValidationError):
        e_msg = e.message

    return jsonify({
        'exception': type(e).__name__,
        'message': e_msg,
        'refId': getattr(e, 'ref_id', "")
    }), code

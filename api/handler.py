from functools import wraps

from flask.json import jsonify

from exceptions.api import ParametersException
from exceptions.service import ServiceError

EXCEPTIONS = {
    ParametersException: 400,
    ValueError: 400,

    ServiceError: 503
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

    return jsonify({
        'exception': type(e).__name__,
        'message': e_msg,
        'refId': getattr(e, 'ref_id', "")
    }), code

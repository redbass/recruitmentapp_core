from functools import wraps

from flask.json import jsonify

from exceptions import api

EXCEPTIONS_400 = [api.ParametersException,
                  api.ArgumentException]


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

    #  400 Bad Request
    if type(e) in EXCEPTIONS_400:
        code = 400

    return jsonify({
        'exception': type(e).__name__,
        'msg': e_msg,
        'refId': getattr(e, 'ref_id', "")
    }), code

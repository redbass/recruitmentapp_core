from functools import wraps

from flask.json import jsonify


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
    return jsonify({
        'error': 'Unexpected error',
        'exception': str(e)
    }), 500

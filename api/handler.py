from functools import wraps
from json import dumps


def json_response(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            result = f(*args, **kwargs)
            return dumps(result), 200

        except Exception as e:
            return _error_handler(e)

    return wrapper


def _error_handler(e):
    return dumps({
        'error': 'Unexpected error',
        'exception': str(e)
    }), 500

from functools import wraps

from flask import request

from exceptions.auth import AuthenticationError

TOKEN = "token"


def api_token_required(fn):

    @wraps(fn)
    def wrapped(*args, **qwargs):
        api_key = request.values.get('apiKey', '')

        if api_key != TOKEN:
            raise AuthenticationError("Invalid api token")
        return fn(*args, ** qwargs)

    return wrapped

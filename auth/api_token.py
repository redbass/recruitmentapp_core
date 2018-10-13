from functools import wraps

from flask import request
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError

from config import settings
from exceptions.auth import AuthenticationError

API_KEI_TOKEN = "token"


def api_token_required(fn):

    @wraps(fn)
    def wrapped(*args, **qwargs):

        try:
            return jwt_required(fn)(*args, **qwargs)
        except NoAuthorizationError:
            pass

        api_key = request.values.get('apiKey', '')

        if api_key != (settings.DEFAULT_API_KEY or API_KEI_TOKEN):
            raise AuthenticationError("Invalid api token")
        return fn(*args, ** qwargs)

    return wrapped

from functools import wraps

from flask import request


def api_key_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        token = request.args['token']
        remote_addr = request.remote_addr

        if is_valid_key(remote_addr, token):

            return fn(*args, **kwargs)

        raise Exception("Wrong token from the remote address '{remote_addr}'"
                        .format(remote_addr=remote_addr))

    return wrapper


def is_valid_key(remote_addr: str, token: str) -> bool:
    return TOKENS.get(remote_addr) == token


TOKENS = {
    '127.0.0.1': 'test_key'
}


from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_refresh_token_required,
    get_jwt_identity, unset_jwt_cookies
)
from flask_jwt_extended import jwt_required as flask_jwt_required, \
    create_refresh_token

from config import settings
from lib.password import check_password
from model.user import get_user

__jwt = None

TEST_IDENTITY = {'username': 'super@user.com'}


def setup_jwt(app) -> JWTManager:
    global __jwt

    if not __jwt:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = \
            settings.JWT_ACCESS_TOKEN_EXPIRES
        # Configure application to store JWTs in cookies
        app.config['JWT_TOKEN_LOCATION'] = ['headers']
        # Only allow JWT cookies to be sent over https. In production, this
        # should likely be True
        app.config['JWT_COOKIE_SECURE'] = False
        # Set the cookie paths, so that you are only sending your access token
        # cookie to the access endpoints, and only sending your refresh token
        # to the refresh endpoint. Technically this is optional, but it is in
        # your best interest to not send additional cookies in the request if
        # they aren't needed.
        app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
        app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'

        # Enable csrf double submit protection. See this for a thorough
        # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
        app.config['JWT_COOKIE_CSRF_PROTECT'] = False

        __jwt = JWTManager(app)

        _setup_endpoints(app)

    return __jwt


def jwt_required(get_identity=False):

    def decorated(fn):

        @wraps(fn)
        def wrapped(*args, **qwargs):

            if not settings.LOGIN_REQUIRED:
                if get_identity:
                    qwargs['identity'] = TEST_IDENTITY
                return fn(*args, **qwargs)

            def jwt_fn():
                identity = get_jwt_identity()
                if get_identity:
                    qwargs['identity'] = identity
                return fn(*args, **qwargs)

            return flask_jwt_required(jwt_fn)()

        return wrapped

    return decorated


def _setup_endpoints(app):

    @app.route('/token/auth', methods=['POST'])
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = get_user(username)
        if not user or not check_password(password, user.get('password')):
            return jsonify({'login': False}), 401

        # Create the tokens we will be sending back to the user
        identity = _create_identity_object(username)
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        # Set the JWTs and the CSRF double submit protection cookies
        # in this response
        resp = jsonify({
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'username': username
        })
        # set_access_cookies(resp, access_token)
        # set_refresh_cookies(resp, refresh_token)
        return resp, 200

    @app.route('/token/refresh', methods=['POST'])
    @jwt_refresh_token_required
    def refresh():
        identity = get_jwt_identity()
        current_user = identity['username']
        ret = {
            'accessToken': create_access_token(
                identity=_create_identity_object(current_user))
        }
        return jsonify(ret), 200

    @app.route('/token/remove', methods=['POST'])
    def logout():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

    def _create_identity_object(username):
        return {"username": username}

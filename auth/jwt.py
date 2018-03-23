from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from auth.user import users

__jwt = None


def setup_jwt(app) -> JWTManager:
    global __jwt

    if not __jwt:
        # Configure application to store JWTs in cookies
        app.config['JWT_TOKEN_LOCATION'] = ['cookies']
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
        app.config['JWT_COOKIE_CSRF_PROTECT'] = True

        __jwt = JWTManager(app)

        _setup_endpoints(app)

    return __jwt


def _setup_endpoints(app):

    @app.route('/token/auth', methods=['POST'])
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = users.get(username, None)
        if not user or not user.check_password(password):
            return jsonify({'login': False}), 401

        # Create the tokens we will be sending back to the user
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        # Set the JWTs and the CSRF double submit protection cookies
        # in this response
        resp = jsonify({'login': True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200

    @app.route('/token/refresh', methods=['POST'])
    @jwt_refresh_token_required
    def refresh():
        # Create the new access token
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        # Set the access JWT and CSRF double submit protection cookies
        # in this response
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return resp, 200

    @app.route('/token/remove', methods=['POST'])
    def logout():
        resp = jsonify({'logout': True})
        unset_jwt_cookies(resp)
        return resp, 200

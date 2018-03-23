from api.job import get_job, create_job
from auth.endpoints import login, logout

JOB_URL = '/api/job'
GET_JOB_URL = JOB_URL + '/<_id>'

LOGIN_URL = "/login"
LOGOUT_URL = "/logout"


def add_routes(app):

    app.add_url_rule(JOB_URL, 'create_job', create_job, methods=['POST'])
    app.add_url_rule(GET_JOB_URL, 'get_job', get_job, methods=['GET'])

    app.add_url_rule(LOGIN_URL, 'login', login, methods=["GET", "POST"])
    app.add_url_rule(LOGOUT_URL, 'logout', logout, methods=["GET", "POST"])


def add_test_routes(app):
    from flask import Response
    from flask_login import login_required

    @app.route('/')
    @login_required
    def home():
        return Response("Hello World!")

    # handle login failed
    @app.errorhandler(401)
    def page_not_found(e):
        return Response('<p>Login failed</p>')

    # handle login failed
    @app.errorhandler(401)
    def page_not_found(e):
        return Response('<p>Login failed</p>')
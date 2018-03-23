from api.job import get_job, create_job
from auth.endpoints import login, logout

JOB_URL = '/api/job'
GET_JOB_URL = JOB_URL + '/<_id>'

LOGIN_URL = JOB_URL + "/login"
LOGOUT_URL = JOB_URL + "/logout"


def add_routes(app):

    app.add_url_rule(JOB_URL, 'create_job', create_job, methods=['POST'])
    app.add_url_rule(GET_JOB_URL, 'get_job', get_job, methods=['GET'])

    app.add_url_rule(LOGIN_URL, 'get_job', login, methods=["GET", "POST"])
    app.add_url_rule(LOGIN_URL, 'get_job', logout, methods=["GET", "POST"])

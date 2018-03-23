from api.job import get_job, create_job

JOB_URL = '/api/job'
GET_JOB_URL = JOB_URL + '/<_id>'


def add_routes(app):

    app.add_url_rule(JOB_URL, 'create_job', create_job, methods=['POST'])
    app.add_url_rule(GET_JOB_URL, 'get_job', get_job, methods=['GET'])

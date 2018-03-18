from api.job import get_job

GET_JOB_URL = '/api/job/<_id>'


def add_routes(app):
    return app.add_url_rule(GET_JOB_URL, 'get_job', get_job, methods=['GET'])

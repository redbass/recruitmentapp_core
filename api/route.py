from api.job import create_job
from api.search import search_adverts_by_radius

JOB_URL = '/api/job'
GET_JOB_URL = JOB_URL + '/<_id>'
GET_ALL_JOBS_URL = JOB_URL
SEARCH_ADVERTS_BY_RADIUS_URL = JOB_URL + '/search/advert/radius'


def add_routes(app):

    _add_job_routes(app)


def _add_job_routes(app):

    app.add_url_rule(JOB_URL,
                     'create_job',
                     create_job,
                     methods=['POST'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search_adverts_by_radius,
                     methods=['GET'])

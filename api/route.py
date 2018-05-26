from api.job import create_job
from api.advert import create_advert
from api.search import search_adverts_by_radius

JOBS_URL = '/api/job'
ADVERTS_URL = '/api/job/<job_id>/advert'

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'


def add_routes(app):

    _add_job_routes(app)


def _add_job_routes(app):

    app.add_url_rule(JOBS_URL,
                     'create_job',
                     create_job,
                     methods=['POST'])

    app.add_url_rule(ADVERTS_URL,
                     'create_advert',
                     create_advert,
                     methods=['POST'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search_adverts_by_radius,
                     methods=['GET'])

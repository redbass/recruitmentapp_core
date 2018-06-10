from api.job import create_job, get_jobs
from api.advert import create_advert, approve_advert
from api.search import search_adverts_by_radius
from api.user import create_user

USERS_URL = '/api/user'
JOBS_URL = '/api/job'
ADVERTS_URL = '/api/job/<job_id>/advert'
APPROVE_ADVERT_URL = '/api/job/<job_id>/advert/<advert_id>/approve'

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'


def add_routes(app):

    app.add_url_rule(JOBS_URL,
                     'get_jobs',
                     get_jobs,
                     methods=['GET'])

    app.add_url_rule(JOBS_URL,
                     'create_job',
                     create_job,
                     methods=['POST'])

    app.add_url_rule(ADVERTS_URL,
                     'create_advert',
                     create_advert,
                     methods=['POST'])

    app.add_url_rule(APPROVE_ADVERT_URL,
                     'approve_advert',
                     approve_advert,
                     methods=['POST'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search_adverts_by_radius,
                     methods=['GET'])

    app.add_url_rule(USERS_URL,
                     'create_user',
                     create_user,
                     methods=['POST'])

from api import job, advert, search, user

USERS_URL = '/api/user'
GET_USERS_BY_TYPE_URL = '/api/user/<user_type>'
JOBS_URL = '/api/job'
ADVERTS_URL = '/api/job/<job_id>/advert'
APPROVE_ADVERT_URL = '/api/job/<job_id>/advert/<advert_id>/approve'

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'


def add_routes(app):

    app.add_url_rule(JOBS_URL,
                     'get_jobs',
                     job.get_jobs,
                     methods=['GET'])

    app.add_url_rule(JOBS_URL,
                     'create_job',
                     job.create_job,
                     methods=['POST'])

    app.add_url_rule(ADVERTS_URL,
                     'create_advert',
                     advert.create_advert,
                     methods=['POST'])

    app.add_url_rule(APPROVE_ADVERT_URL,
                     'approve_advert',
                     advert.approve_advert,
                     methods=['POST'])

    app.add_url_rule(USERS_URL,
                     'create_user',
                     user.create_user,
                     methods=['POST'])

    app.add_url_rule(GET_USERS_BY_TYPE_URL,
                     'get_users',
                     user.get_users,
                     methods=['GET'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search.search_adverts_by_radius,
                     methods=['GET'])

from api import job, advert, search, user, company

USERS_URL = '/api/user'
GET_USERS_BY_TYPE_URL = '/api/user/<user_type>'

COMPANIES_URL = '/api/company'
COMPANY_URL = '/api/company/<company_id>'

JOBS_URL = '/api/job'

ADVERTS_URL = '/api/job/<job_id>/advert'
APPROVE_ADVERT_URL = '/api/job/<job_id>/advert/<advert_id>/approve'

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'

ADMIN_COMPANIES_URL = '/admin/api/company'
ADMIN_JOBS_URL = '/admin/api/job'


def add_routes(app):

    add_job_routes(app)
    add_user_routes(app)
    add_company_routes(app)

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search.search_adverts_by_radius,
                     methods=['GET'])


def add_company_routes(app):

    app.add_url_rule(COMPANIES_URL,
                     'create_company',
                     company.create_company,
                     methods=['POST'])

    app.add_url_rule(ADMIN_COMPANIES_URL,
                     'admin_create_company',
                     company.admin_create_company,
                     methods=['POST'])

    app.add_url_rule(COMPANIES_URL,
                     'get_companies',
                     company.get_companies,
                     methods=['GET'])

    app.add_url_rule(COMPANY_URL,
                     'get_company',
                     company.get_company,
                     methods=['GET'])


def add_job_routes(app):
    app.add_url_rule(JOBS_URL,
                     'get_jobs',
                     job.get_jobs,
                     methods=['GET'])
    app.add_url_rule(ADMIN_JOBS_URL,
                     'admin_create_job',
                     job.admin_create_job,
                     methods=['POST'])

    app.add_url_rule(ADVERTS_URL,
                     'create_advert',
                     advert.create_advert,
                     methods=['POST'])
    app.add_url_rule(APPROVE_ADVERT_URL,
                     'approve_advert',
                     advert.approve_advert,
                     methods=['POST'])


def add_user_routes(app):

    app.add_url_rule(GET_USERS_BY_TYPE_URL,
                     'get_users',
                     user.get_users,
                     methods=['GET'])

import api.company.admin_company
from api import job, advert, user

ADMIN_PREFIX = 'admin'

COMPANIES_URL = '/api/company'
COMPANY_URL = '/api/company/<company_id>'
JOBS_URL = '/api/job'
ADVERTS_URL = '/api/job/<job_id>/advert'
APPROVE_ADVERT_URL = '/api/job/<job_id>/advert/<advert_id>/approve'

GET_USERS_BY_TYPE_URL = '/api/user/<user_type>'


def add_admin_routes(app):
    _add_job_routes(app)
    _add_user_routes(app)
    _add_company_routes(app)


def _add_company_routes(app):
    _add_admin_url_rule(app,
                        COMPANIES_URL,
                        'create_company',
                        api.company.admin_company.create_company,
                        methods=['POST'])

    _add_admin_url_rule(app,
                        COMPANIES_URL,
                        'get_companies',
                        api.company.admin_company.get_companies,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        COMPANY_URL,
                        'get_company',
                        api.company.admin_company.get_company,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        COMPANY_URL,
                        'edit_company',
                        api.company.admin_company.edit_company,
                        methods=['POST'])


def _add_job_routes(app):
    _add_admin_url_rule(app,
                        JOBS_URL,
                        'get_jobs',
                        job.get_jobs,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        JOBS_URL,
                        'create_job',
                        job.admin_create_job,
                        methods=['POST'])

    _add_admin_url_rule(app,
                        ADVERTS_URL,
                        'create_advert',
                        advert.create_advert,
                        methods=['POST'])
    _add_admin_url_rule(app,
                        APPROVE_ADVERT_URL,
                        'approve_advert',
                        advert.approve_advert,
                        methods=['POST'])


def _add_user_routes(app):
    _add_admin_url_rule(app,
                        GET_USERS_BY_TYPE_URL,
                        'get_users',
                        user.get_users,
                        methods=['GET'])


def _add_admin_url_rule(app, rule, endpoint=None, view_func=None, **options):
    rule = "/{prefix}{rule}".format(prefix=ADMIN_PREFIX, rule=rule)
    endpoint = "{prefix}_{endpoint}".format(prefix=ADMIN_PREFIX,
                                            endpoint=endpoint)

    app.add_url_rule(rule, endpoint, view_func, **options)

import api.company.admin_company
import api.job.admin_job
from api import user

ADMIN_PREFIX = 'admin'

COMPANIES_URL = '/api/company'
COMPANY_URL = '/api/company/<company_id>'
COMPANY_ACTIONS_URL = '/api/company/<company_id>/<action>'
JOBS_URL = '/api/job'
JOB_URL = '/api/job/<job_id>'
JOB_APPLICATIONS = '/api/job/<job_id>/applications'
ADVERTS_URL = '/api/job/<job_id>/advert'
SET_ADVERT_STATUS_URL = '/api/job/<job_id>/advert/<advert_id>/<action>'
PAY_ADVERT_URL = '/api/job/<job_id>/advert/<advert_id>/pay'

USERS_URL = '/api/user'
USER_URL = '/api/user/<user_id>'


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

    _add_admin_url_rule(app,
                        COMPANY_ACTIONS_URL,
                        'company_actions',
                        api.company.admin_company.company_actions,
                        methods=['POST'])


def _add_job_routes(app):
    _add_admin_url_rule(app,
                        JOBS_URL,
                        'get_jobs',
                        api.job.admin_job.api_get_jobs,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        JOB_URL,
                        'get_job',
                        api.job.admin_job.api_get_job,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        JOBS_URL,
                        'create_job',
                        api.job.admin_job.api_create_job,
                        methods=['POST'])

    _add_admin_url_rule(app,
                        JOB_URL,
                        'edit_job',
                        api.job.admin_job.api_edit_job,
                        methods=['POST'])

    _add_admin_url_rule(app,
                        JOB_APPLICATIONS,
                        'get_advert_applications',
                        api.job.admin_job.api_get_advert_applications,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        ADVERTS_URL,
                        'create_advert',
                        api.job.admin_job.api_add_advert_to_job,
                        methods=['POST'])
    _add_admin_url_rule(app,
                        SET_ADVERT_STATUS_URL,
                        'set_advert_status',
                        api.job.admin_job.set_advert_status,
                        methods=['POST'])


def _add_user_routes(app):
    _add_admin_url_rule(app,
                        USERS_URL,
                        'get_users',
                        user.get_users,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        USER_URL,
                        'get_user',
                        user.get_user,
                        methods=['GET'])

    _add_admin_url_rule(app,
                        USER_URL,
                        'set_password',
                        user.update_password,
                        methods=['POST'])


def _add_admin_url_rule(app, rule, endpoint=None, view_func=None, **options):
    rule = "/{prefix}{rule}".format(prefix=ADMIN_PREFIX, rule=rule)
    endpoint = "{prefix}_{endpoint}".format(prefix=ADMIN_PREFIX,
                                            endpoint=endpoint)

    app.add_url_rule(rule, endpoint, view_func, **options)

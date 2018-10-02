from api.company import hm_company
from api.job import hm_job

COMPANIES_URL = '/api/company'
COMPANY_JOBS_URL = '/api/hm/company/job'


def add_hiring_manager_routes(app):
    app.add_url_rule(COMPANIES_URL,
                     'sign_in_company',
                     hm_company.sign_in_company,
                     methods=['POST'])

    app.add_url_rule(COMPANY_JOBS_URL,
                     'company_jobs',
                     hm_job.api_get_company_jobs,
                     methods=['GET'])

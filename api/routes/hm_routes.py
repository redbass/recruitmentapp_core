from api.job import hm_job

COMPANY_JOBS_URL = '/api/hm/company/job'


def add_hiring_manager_routes(app):

    app.add_url_rule(COMPANY_JOBS_URL,
                     'company_jobs',
                     hm_job.api_get_company_jobs,
                     methods=['GET'])

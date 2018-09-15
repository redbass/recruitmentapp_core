from api.company import hr_company

COMPANIES_URL = '/api/company'


def add_hiring_manager_routes(app):
    app.add_url_rule(COMPANIES_URL,
                     'create_company',
                     hr_company.sign_in_company,
                     methods=['POST'])

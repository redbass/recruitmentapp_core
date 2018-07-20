from api import search
from api.company import company

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'
SEARCH = '/api/job/search'

COMPANIES_URL = '/api/company'


def add_public_routes(app):
    app.add_url_rule(COMPANIES_URL,
                     'create_company',
                     company.create_company,
                     methods=['POST'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search.search_adverts_by_radius,
                     methods=['GET'])

    app.add_url_rule(SEARCH,
                     'search',
                     search.search,
                     methods=['GET'])

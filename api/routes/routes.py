from api.company import company
from api.services import postcode, picklist, search

SEARCH_ADVERTS_BY_RADIUS_URL = '/api/job/search/advert/radius'
SEARCH_STATIC = '/api/job/search_static'
SEARCH = '/api/job/search'

COMPANIES_URL = '/api/company'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'


def add_public_routes(app):
    app.add_url_rule(COMPANIES_URL,
                     'create_company',
                     company.create_company,
                     methods=['POST'])

    app.add_url_rule(SEARCH_ADVERTS_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search.search_adverts_by_radius,
                     methods=['GET'])

    app.add_url_rule(SEARCH_STATIC,
                     'search_static',
                     search.search_static,
                     methods=['GET'])

    app.add_url_rule(SEARCH,
                     'search',
                     search.search,
                     methods=['GET'])

    app.add_url_rule(PICKLIST,
                     'picklist',
                     picklist.picklist,
                     methods=['GET'])

    app.add_url_rule(POSTCODE_SEARCH,
                     'postcode',
                     postcode.get_postcode)

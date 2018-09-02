from api.company import company
from api.services import postcode, picklist, search

SEARCH_STATIC = '/api/job/search_static'
SEARCH = '/api/job/search'

COMPANIES_URL = '/api/company'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'


def add_public_routes(app):
    _add_service_routes(app)
    app.add_url_rule(COMPANIES_URL,
                     'create_company',
                     company.create_company,
                     methods=['POST'])


def _add_service_routes(app):

    app.add_url_rule(SEARCH_STATIC,
                     'search_static',
                     search.search_static,
                     methods=['GET'])
    app.add_url_rule(SEARCH,
                     'search',
                     search.api_search,
                     methods=['GET'])

    app.add_url_rule(PICKLIST,
                     'picklist',
                     picklist.picklist,
                     methods=['GET'])

    app.add_url_rule(POSTCODE_SEARCH,
                     'postcode',
                     postcode.get_postcode)

from api.services import postcode, picklist, search

SEARCH_STATIC = '/api/job/search_static'
SEARCH = '/api/job/search'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'


def add_service_routes(app):

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

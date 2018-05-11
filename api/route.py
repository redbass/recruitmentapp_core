from api.advert import get_advert, create_adverts, get_all_adverts
from api.search import search_advert_by_radius

ADVERT_URL = '/api/advert'
GET_ADVERT_URL = ADVERT_URL + '/<_id>'
GET_ALL_ADVERTS_URL = ADVERT_URL
SEARCH_ADVERT_BY_RADIUS_URL = ADVERT_URL + '/search/radius'


def add_routes(app):

    app.add_url_rule(ADVERT_URL,
                     'create_advert',
                     create_adverts,
                     methods=['POST'])

    app.add_url_rule(GET_ADVERT_URL,
                     'get_advert',
                     get_advert,
                     methods=['GET'])

    app.add_url_rule(GET_ALL_ADVERTS_URL,
                     'get_all_adverts',
                     get_all_adverts,
                     methods=['GET'])

    app.add_url_rule(SEARCH_ADVERT_BY_RADIUS_URL,
                     'search_advert_by_radius',
                     search_advert_by_radius,
                     methods=['GET'])

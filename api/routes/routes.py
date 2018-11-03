from api.services import postcode, picklist, search, stripe_webhooks
from api.company import company

SEARCH_STATIC = '/api/job/search_static'
SEARCH = '/api/job/search'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'

COMPANY_LOGO = '/api/company/<company_id>/logo'

STRIPE_WEBHOOK_CHARGE = '/api/job/charge'


def add_generic_routes(app):

    _add_services_routes(app)
    _add_company_routes(app)


def _add_services_routes(app):
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
                     postcode.get_postcode,
                     methods=['GET'])
    app.add_url_rule(STRIPE_WEBHOOK_CHARGE,
                     'stripe_webhook_charge',
                     stripe_webhooks.publish_advert_by_stripe_webhook_charge,
                     methods=['POST'])


def _add_company_routes(app):
    app.add_url_rule(COMPANY_LOGO,
                     'upload_company_logo',
                     company.upload_company_logo,
                     methods=['POST'])

    app.add_url_rule(COMPANY_LOGO,
                     'get_company_logo',
                     company.get_company_logo,
                     methods=['GET'])

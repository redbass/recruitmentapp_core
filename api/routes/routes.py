from api.services import postcode, picklist, search
from api.integration import stripe
from api.company import company

SEARCH_STATIC = '/api/job/search_static'
SEARCH = '/api/job/search'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'

COMPANY_LOGO = '/api/company/<company_id>/logo'

STRIPE_CHARGE_PAYMENT = '/api/stripe/charge'
STRIPE_CHARGE_PROCESSED = '/api/stripe/charge/processed'


def add_generic_routes(app):

    _add_services_routes(app)
    _add_integration_routes(app)
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


def _add_integration_routes(app):
    app.add_url_rule(STRIPE_CHARGE_PAYMENT,
                     'stripe_charge_payment',
                     stripe.charge_payment,
                     methods=['POST'])
    app.add_url_rule(STRIPE_CHARGE_PROCESSED,
                     'stripe_charge_processed',
                     stripe.charge_processed,
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

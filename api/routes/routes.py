from api.services import postcode, search
from api import picklist
from api.integration import stripe
from api.company import company, hm_company

SEARCH = '/api/job/search'

PICKLIST = '/api/picklist/<name>'

POSTCODE_SEARCH = '/api/postcode/<postcode>'

COMPANY_LOGO = '/api/company/<company_id>/logo'
COMPANIES_URL = '/api/company'

STRIPE_GET_CONFIG = '/api/stripe/config'
STRIPE_CHARGE_PAYMENT = '/api/stripe/charge'
STRIPE_CHARGE_PROCESSED = '/api/stripe/charge/processed'


def add_generic_routes(app):

    _add_services_routes(app)
    _add_integration_routes(app)

    app.add_url_rule(COMPANY_LOGO,
                     'upload_company_logo',
                     company.upload_company_logo,
                     methods=['POST'])

    app.add_url_rule(COMPANY_LOGO,
                     'get_company_logo',
                     company.get_company_logo,
                     methods=['GET'])

    app.add_url_rule(COMPANIES_URL,
                     'sign_in_company',
                     hm_company.sign_in_company,
                     methods=['POST'])

    app.add_url_rule(PICKLIST,
                     'get_picklist',
                     picklist.get_picklist,
                     methods=['GET'])

    app.add_url_rule(PICKLIST,
                     'store_picklist',
                     picklist.store_picklist,
                     methods=['POST'])


def _add_services_routes(app):
    app.add_url_rule(SEARCH,
                     'search',
                     search.api_search,
                     methods=['GET'])
    app.add_url_rule(POSTCODE_SEARCH,
                     'postcode',
                     postcode.get_postcode,
                     methods=['GET'])


def _add_integration_routes(app):
    app.add_url_rule(STRIPE_GET_CONFIG,
                     'stripe_cget_config',
                     stripe.get_stripe_config,
                     methods=['GET'])
    app.add_url_rule(STRIPE_CHARGE_PAYMENT,
                     'stripe_charge_payment',
                     stripe.charge_payment,
                     methods=['POST'])
    app.add_url_rule(STRIPE_CHARGE_PROCESSED,
                     'stripe_charge_processed',
                     stripe.charge_processed,
                     methods=['POST'])

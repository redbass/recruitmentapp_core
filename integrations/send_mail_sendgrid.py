from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import settings
from db.collections import configs
from exceptions.integrations import SendgridException
from model.company.company import get_company


class SendgridConfig:

    def __init__(self):
        sendgrid_config = configs.find_one({'_id': 'sendgrid'})
        self.api_key = settings.SENDGRID_SECRET_KEY
        self.admin_email_address = sendgrid_config['admin_email_address']
        self.company_accepted_template = \
            sendgrid_config['company_accepted_template']


def send_email(from_email, to_emails, template_id, api_key,
               template_data=None):
    try:
        message = Mail(from_email=from_email, to_emails=to_emails)
        message.dynamic_template_data = template_data or {}
        message.template_id = template_id

        SendGridAPIClient(api_key).send(message)
    except Exception as e:
        raise SendgridException(e)


def send_email_company_approved(company_id):
    sendgrid_settings = SendgridConfig()
    company = get_company(company_id=company_id)

    send_email(from_email=sendgrid_settings.admin_email_address,
               to_emails=company['contacts']['email'],
               template_id=sendgrid_settings.company_accepted_template,
               api_key=sendgrid_settings.api_key,
               template_data=company)

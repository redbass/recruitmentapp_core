from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import settings
from db.collections import configs
from exceptions import BaseRecruitmentAppException
from exceptions.integrations import SendgridException
from model.company.company import get_company
from model.job.job import get_job


class SendgridConfig:

    def __init__(self):
        sendgrid_config = self._get_config()
        self.api_key = settings.SENDGRID_SECRET_KEY
        self.admin_email_address = sendgrid_config.get('admin_email_address')
        self.company_accepted_template = \
            sendgrid_config.get('company_accepted_template')
        self.advert_approved_template = \
            sendgrid_config.get('advert_approved_template')

    def _get_config(self):
        sendgrid_config = configs.find_one({'_id': 'sendgrid'})

        if not sendgrid_config and not settings.TEST_MODE:
            raise BaseRecruitmentAppException("Sendgrid configuration missing")

        return sendgrid_config or {}


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
               template_data={
                   'company': company
               })


def send_email_advert_approved(job_id):
    sendgrid_settings = SendgridConfig()

    job = get_job(job_id=job_id)
    company = get_company(company_id=job['company_id'])

    send_email(from_email=sendgrid_settings.admin_email_address,
               to_emails=company['contacts']['email'],
               template_id=sendgrid_settings.advert_approved_template,
               api_key=sendgrid_settings.api_key,
               template_data={
                   'company': company,
                   'job': {
                       'title': job['title'],
                       'description': job['description']
                   }
               })

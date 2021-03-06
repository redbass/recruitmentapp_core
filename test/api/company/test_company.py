from io import BytesIO
from json import loads

from api.routes.routes import COMPANIES_URL
from api.routes.routes import COMPANY_LOGO
from model.company.company import store_company_logo, get_company_logo
from model.user import get_user, UserType
from test import load_example_model
from test.api.company import BaseTestCompany
from test.model.company import CompanyFactory
from test.model.test_user import UserFactory


class TestGetCompanyLogo(BaseTestCompany):

    def setUp(self):
        super().setUp()
        self.company = self.create_from_factory(CompanyFactory)

    def test_get_company_logo(self):
        company_logo = BytesIO("image".encode('utf-8'))
        store_company_logo(company_id=self.company['_id'], file=company_logo)

        url = self.url_for(COMPANY_LOGO, company_id=self.company['_id'])
        response = self.get_data(url)

        self.assertEqual(200, response.status_code)

        company_logo.seek(0)
        self.assertEquals(company_logo.read(), response.data)

    def test_get_company_logo_invalid_company_id(self):
        company_logo = BytesIO("image".encode('utf-8'))
        store_company_logo(company_id=self.company['_id'], file=company_logo)

        url = self.url_for(COMPANY_LOGO, company_id="123123123123123")
        response = self.get_data(url)

        self.assertEqual(200, response.status_code)


class TestUploadCompanyLogo(BaseTestCompany):

    def setUp(self):
        super().setUp()
        self.company = self.create_from_factory(CompanyFactory)

    def test_upload_company_logo(self):
        company_logo_content = "this is an image".encode('utf-8')

        url = self.url_for(COMPANY_LOGO, company_id=self.company['_id'])
        response = self.post_data(
            url, buffered=True, content_type='multipart/form-data',
            data={'file': (BytesIO(company_logo_content), 'test.txt')})

        self.assertEqual(200, response.status_code)

        stored_logo = get_company_logo(company_id=self.company['_id'])

        self.assertEquals(company_logo_content, stored_logo.read())

    def test_upload_company_logo_for_invalid_company_id(self):
        company_logo_content = "this is an image".encode('utf-8')

        url = self.url_for(COMPANY_LOGO, company_id=self.company['_id'])
        response = self.post_data(
            url, buffered=True, content_type='multipart/form-data',
            data={'file': (BytesIO(company_logo_content), 'test.txt')})

        self.assertEqual(200, response.status_code)

    def test_hm_can_update_only_own_company_logo(self):
        response = self._upload_file_as(user_type=UserType.HIRING_MANAGER)
        self.assertEqual(200, response.status_code)

    def test_hm_cannot_update_other_company_logo(self):
        response = self._upload_file_as(user_type=UserType.HIRING_MANAGER,
                                        company_id=self.company['_id'])
        self.assertEqual(405, response.status_code)

    def _upload_file_as(self, user_type, company_id=None):
        self._user = self.create_from_factory(
            UserFactory, username=user_type + "@test.com", user_type=user_type)

        company = self.create_from_factory(CompanyFactory,
                                           admin_user_ids=[self._user['_id']])

        company_logo_content = "this is an image".encode('utf-8')

        url = self.url_for(COMPANY_LOGO,
                           company_id=company_id or company['_id'])
        response = self.post_data(
            url, buffered=True, content_type='multipart/form-data',
            data={'file': (BytesIO(company_logo_content), 'test.txt')})

        return response


class TestHMCompany(BaseTestCompany):

    def test_sign_in_company(self):

        input_data = load_example_model('sign_in_company')

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, input_data)

        self.assertEqual(200, response.status_code)

        result_company = loads(response.data)
        stored_company_id = result_company['admin_user_ids'][0]

        self.assertEqual(input_data['company_name'], result_company['name'])
        self.assertEqual(input_data['company_description'],
                         result_company['description'])

        stored_hm = get_user(stored_company_id)
        self.assertIsNotNone(stored_hm)
        self.assertEqual(stored_hm['type'], UserType.HIRING_MANAGER)

        self.assertEqual(input_data['hm_email'],
                         result_company['contacts']['email'])

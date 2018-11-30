from json import loads
from unittest.mock import patch

from api.routes.admin_routes import COMPANIES_URL, COMPANY_URL, \
    COMPANY_ACTIONS_URL
from auth.jwt import TEST_IDENTITY
from model.company.company import get_company
from test import load_example_model
from test.api.company import BaseTestCompany
from test.model.company import CompanyFactory
from test.model.test_user import UserFactory


class TestCreateCompany(BaseTestCompany):

    def test_create_company(self):
        self.create_from_factory(UserFactory,
                                 username=TEST_IDENTITY['username'])
        data = load_example_model('create_company_input')

        url = self.url_for_admin(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        result_company = loads(response.data)

        self.assertEqual(data['name'], result_company['name'])
        self.assertEqual(data['description'], result_company['description'])


class TestEditCompany(BaseTestCompany):

    def test_edit_company(self):
        company = self.create_from_factory(CompanyFactory)

        data = {
            "name": "ACME Inc.",
            "description": "Some description"
        }

        url = self.url_for_admin(COMPANY_URL, company_id=company['_id'])
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        result_company = loads(response.data)

        self.assertEqual(data['name'], result_company['name'])
        self.assertEqual(data['description'],
                         result_company['description'])

    def test_enable_disable_company(self):
        company = self.create_from_factory(CompanyFactory)

        self.assertFalse(company['enabled'])

        url = self.url_for_admin(COMPANY_ACTIONS_URL,
                                 action='enable',
                                 company_id=company['_id'])
        self.post_json(url)
        company = get_company(company['_id'])
        self.assertTrue(company['enabled'])

        url = self.url_for_admin(COMPANY_ACTIONS_URL,
                                 action='disable',
                                 company_id=company['_id'])
        self.post_json(url)
        company = get_company(company['_id'])
        self.assertFalse(company['enabled'])

    def test_company_actions_not_supported_raise_error(self):
        company = self.create_from_factory(CompanyFactory)

        url = self.url_for_admin(COMPANY_ACTIONS_URL,
                                 action='random',
                                 company_id=company['_id'])
        response = self.post_json(url)

        self.assertEquals(400, response.status_code)


class TestGetCompany(BaseTestCompany):

    @patch('api.company.admin_company.company')
    def test_get_companies(self, company_mock):

        url = self.url_for_admin(COMPANIES_URL, )
        response = self.get_data(url)

        self.assertEqual(200, response.status_code)
        company_mock.get_companies.assert_called_once()

    @patch('api.company.admin_company.company')
    def test_get_company(self, company_mock):
        company_id = '1'
        url = self.url_for_admin(COMPANY_URL, company_id=company_id)
        response = self.get_data(url)

        self.assertEqual(200, response.status_code)
        company_mock.get_company.assert_called_with(company_id=company_id)

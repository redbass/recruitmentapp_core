from unittest.mock import patch

from api.routes.admin_routes import COMPANIES_URL, COMPANY_URL
from test import load_example_model
from test.api import TestApi
from test.model.company import CompanyFactory
from test.model.user import UserFactory


class TestCreateCompany(TestApi):

    def test_create_company(self):
        self.create_from_factory(UserFactory, username='super_user')
        data = load_example_model('create_company_input')

        url = self.url_for_admin(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)


class TestEditCompany(TestApi):

    def test_edit_company(self):
        company = self.create_from_factory(CompanyFactory)

        data = {
            "name": "ACME Inc.",
            "description": "Some description"
        }

        url = self.url_for_admin(COMPANY_URL, company_id=company['_id'])
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)


class TestGetCompany(TestApi):

    @patch('api.company.admin_company.company')
    def test_get_companies(self, company_mock):

        url = self.url_for_admin(COMPANIES_URL, )
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        company_mock.get_companies.assert_called_once()

    @patch('api.company.admin_company.company')
    def test_get_company(self, company_mock):
        company_id = '1'
        url = self.url_for_admin(COMPANY_URL, company_id=company_id)
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        company_mock.get_company.assert_called_with(company_id=company_id)

from unittest.mock import patch

from api.routes.admin_routes import COMPANIES_URL, COMPANY_URL
from model import NOT_PROVIDED
from test.api import TestApi


class TestCreateCompany(TestApi):

    @patch('api.company.admin_company.company')
    @patch('api.company.admin_company.user')
    def test_create_company(self, user_mock, company_mock):
        data = {
            "name": "ACME Inc.",
            "description": "Some description"
        }
        super_user = 'super_user'
        user_mock.get_user.return_value = {"_id": super_user}
        company_mock.create_company.return_value = {"company": "created"}

        url = self.url_for_admin(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        company_mock.create_company.assert_called_once_with(
            name=data['name'],
            description=data['description'],
            admin_user_id=super_user)


class TestEditCompany(TestApi):

    @patch('api.company.admin_company.edit_company_model')
    def test_edit_company(self, edit_company):
        company_id = "123"

        data = {
            "company_id": company_id,
            "name": "ACME Inc.",
            "description": "Some description"
        }

        url = self.url_for_admin(COMPANY_URL, company_id=company_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        edit_company.edit_company.assert_called_once_with(
            company_id=company_id,
            new_name=data['name'],
            new_description=data['description'])

    @patch('api.company.admin_company.edit_company_model')
    def test_edit_company_NOT_PROVIDED_if_name_not_set(self, edit_company):
        company_id = "123"

        data = {
            "company_id": company_id,
            "name": "ACME Inc."
        }

        url = self.url_for_admin(COMPANY_URL, company_id=company_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        edit_company.edit_company.assert_called_once_with(
            company_id=company_id,
            new_name=data['name'],
            new_description=NOT_PROVIDED)

    @patch('api.company.admin_company.edit_company_model')
    def test_edit_company_NOT_PROVIDED_if_description_not_set(self,
                                                              edit_company):
        company_id = "123"

        data = {
            "company_id": company_id,
            "description": "Some description"
        }

        url = self.url_for_admin(COMPANY_URL, company_id=company_id)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        edit_company.edit_company.assert_called_once_with(
            company_id=company_id,
            new_name=NOT_PROVIDED,
            new_description=data['description'])


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

from unittest.mock import patch

from api.route import COMPANIES_URL, ADMIN_COMPANIES_URL
from model.user import UserType
from test.api import TestApi


class TestAdminCreateCompany(TestApi):

    @patch('api.company.company')
    @patch('api.company.user')
    def test_admin_create_company(self, user_mock, company_mock):
        data = {
            "name": "ACME Inc.",
            "description": "Some description"
        }
        super_user = 'super_user'
        user_mock.get_user.return_value = {"_id": super_user}
        company_mock.create_company.return_value = {"company": "created"}

        url = self.url_for(ADMIN_COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        company_mock.create_company.assert_called_once_with(
            name=data['name'],
            description=data['description'],
            admin_user_id=super_user)


class TestCreateCompany(TestApi):

    @patch('api.company.company')
    @patch('api.company.user')
    def test_create_company(self, user_mock, company_mock):
        data = {
            "name": "ACME Inc.",
            "description": "Some description",
            "username": "some_user",
            "email": "some@email.test",
            "password": "new_password"
        }
        user_mock.create_user.return_value = {"_id": data['username']}
        company_mock.create_company.return_value = {"company": "created"}

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        user_mock.create_user.assert_called_once_with(
            email=data['email'],
            password=data['password'],
            user_type=UserType.HIRING_MANAGER,
            username=data['username']
        )

        company_mock.create_company.assert_called_once_with(
            name=data['name'],
            description=data['description'],
            admin_user_id=data['username'])

    def test_create_company_no_email_raise_return_error(self):
        data = {
            "name": "Some",
            "description": "Some description",
            "email": "",
            "password": "new_password"
        }

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assert_error(response,
                          400,
                          "Username, email, password are all required")

    def test_create_company_no_password_raise_return_error(self):
        data = {
            "name": "Some",
            "description": "Some description",
            "email": "email@io.com",
            "password": ""
        }

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assert_error(response,
                          400,
                          "Username, email, password are all required")

    @patch('api.company.user')
    def test_create_company_no_company_name_raise_return_error(self, _):
        data = {
            "name": "",
            "description": "Some description",
            "email": "email@io.com",
            "password": "password"
        }

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assert_error(response,
                          400,
                          "Company `name` is a required field")


class TestGetCompany(TestApi):

    @patch('api.company.company')
    def test_create_company(self, company_mock):

        url = self.url_for(COMPANIES_URL)
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        company_mock.get_companies.assert_called_once()

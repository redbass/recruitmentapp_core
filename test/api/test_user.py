from unittest.mock import patch

from api.route import USERS_URL
from model.user import UserType
from test.api import TestApi


class TestAPICreateUser(TestApi):

    @patch('api.user.user')
    def test_create_user(self, mock_user):
        mock_user.create_user.return_value = ""
        email = 'email@some.it'
        password = 'some_password'
        user_type = UserType.ADMIN

        data = {
            'email': email,
            'password': password,
            'user_type': user_type
        }
        response = self.post_json(USERS_URL, data)
        self.assertEqual(200, response.status_code)
        mock_user.create_user.assert_called_with(
            email=email, password=password, user_type=user_type
        )

    @patch('api.user.user')
    def test_create_user_without_passing_user_type(self, mock_user):
        mock_user.create_user.return_value = ""
        email = 'email@some.it'
        password = 'some_password'
        user_type = UserType.CANDIDATE

        data = {
            'email': email,
            'password': password
        }
        response = self.post_json(USERS_URL, data)
        self.assertEqual(200, response.status_code)
        mock_user.create_user.assert_called_with(
            email=email, password=password, user_type=user_type
        )

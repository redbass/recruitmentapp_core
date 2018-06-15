from json import loads
from unittest.mock import patch

from api.route import USERS_URL, GET_USERS_BY_TYPE_URL
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
            'user_type': user_type.lower()
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


class TestAPIGetUsers(TestApi):

    @patch('api.user.user')
    def test_get_users(self, mock_user):

        expected_users = []
        mock_user.get_user.returns = [{"an": "array"}]
        user_type = UserType.ADMIN

        url = self.url_for(GET_USERS_BY_TYPE_URL, user_type=user_type.lower())
        response = self.get_json(url)

        self.assertEqual(200, response.status_code)
        mock_user.get_users.assert_called_with(user_type=user_type)
        self.assertEqual(loads(response.data), expected_users)

    def test_get_users_error_with_wrong_user_type(self):
        user_type = "ABC"
        url = self.url_for(GET_USERS_BY_TYPE_URL, user_type=user_type)
        response = self.get_json(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            loads(response.data)['message'],
            'Invalid user_type `{user_type}`'.format(user_type=user_type))

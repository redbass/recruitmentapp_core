from json import loads
from unittest.mock import patch

from api.route import GET_USERS_BY_TYPE_URL
from model.user import UserType
from test.api import TestApi


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

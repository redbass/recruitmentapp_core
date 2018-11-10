from json import loads

from api.routes.admin_routes import GET_USERS_BY_TYPE_URL, GET_USERS_URL
from model.user import UserType
from test.api import TestApi
from test.model.user import UserFactory


class TestAPIGetUsers(TestApi):

    def setUp(self):
        super().setUp()
        self.user_1 = self.create_from_factory(
            UserFactory, user_type=UserType.ADMIN)
        self.user_2 = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)
        self.user_3 = self.create_from_factory(
            UserFactory, user_type=UserType.CANDIDATE)

    def test_get_users_by_type(self):
        expected_users = [self._user, self.user_1]
        user_type = UserType.ADMIN
        url = self.url_for_admin(GET_USERS_BY_TYPE_URL, user_type=user_type)

        self._assert_get_users(expected_users, url)

    def test_get_users(self):
        expected_users = [self._user, self.user_1, self.user_2, self.user_3]
        url = self.url_for_admin(GET_USERS_URL)

        self._assert_get_users(expected_users, url)

    def test_get_users_error_with_wrong_user_type(self):
        user_type = "ABC"
        url = self.url_for_admin(GET_USERS_BY_TYPE_URL, user_type=user_type)
        response = self.get_data(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            loads(response.data)['message'],
            'Invalid user_type `{user_type}`'.format(user_type=user_type))

    def _assert_get_users(self, expected_users, url):
        expected_users_ids = [user['_id'] for user in expected_users]
        response = self.get_data(url)
        result_users_ids = [user['_id'] for user in loads(response.data)]
        self.assertEqual(200, response.status_code)
        self.assertEqual(result_users_ids, expected_users_ids)

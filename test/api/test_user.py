from json import loads

from api.routes.admin_routes import USERS_URL, USER_URL
from lib.password import check_user_password
from model.user import UserType, get_user
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
        url = self._get_user_by_type_utl(UserType.ADMIN)

        self._assert_get_users(expected_users, url)

    def test_get_users(self):
        expected_users = [self._user, self.user_1, self.user_2, self.user_3]
        url = self.url_for_admin(USERS_URL)

        self._assert_get_users(expected_users, url)

    def test_get_users_error_with_wrong_user_type(self):
        user_type = "ABC"
        url = self._get_user_by_type_utl(user_type)
        response = self.get_data(url)

        self.assertEqual(400, response.status_code)
        self.assertEqual(
            loads(response.data)['message'],
            'Invalid user_type `{user_type}`'.format(user_type=user_type))

    def test_get_user(self):
        user_id = self._user['_id']
        url = self.url_for_admin(USER_URL, user_id=user_id)
        response = self.get_data(url)
        response_user = loads(response.data)

        self.assertEquals(user_id, response_user['_id'])

    def test_get_user_no_results(self):

        url = self.url_for_admin(USER_URL, user_id='random')
        response = self.get_data(url)

        self.assertIsNone(loads(response.data))

    def _assert_get_users(self, expected_users, url):
        expected_users_ids = [user['_id'] for user in expected_users]
        response = self.get_data(url)
        result_users_ids = [user['_id'] for user in loads(response.data)]
        self.assertEqual(200, response.status_code)
        self.assertEqual(result_users_ids, expected_users_ids)

    def _get_user_by_type_utl(self, user_type):
        url_user_type = "?type={user_type}".format(user_type=user_type)
        return self.url_for_admin(USERS_URL) + url_user_type


class TestAPIUpdateUserPassword(TestApi):

    def test_update_password(self):
        user_1 = self.create_from_factory(UserFactory)
        new_password = "new_password"

        self.assertFalse(check_user_password(new_password,
                                             user_1['password']))

        url = self.url_for_admin(USER_URL, user_id=user_1['_id'])
        response = self.post_json(url, data={'password': new_password})

        self.assertEqual(200, response.status_code)

        stored_user = get_user(user_1['_id'])

        self.assertTrue(check_user_password(new_password,
                                            stored_user['password']))

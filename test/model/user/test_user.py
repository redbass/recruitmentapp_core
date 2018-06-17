from db.collections import users
from lib.password import check_password
from model.user import create_user, UserType, get_users, get_user
from test import UnitTestCase


class BaseUserTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.username = "acme_inc"
        self.email = "email@one.it"
        self.password = "some_password"

    def tearDown(self):
        super().tearDown()
        users.drop()


class GetUserTestCase(BaseUserTestCase):

    def test_get_users(self):
        create_user1 = create_user(username="a_" + self.username,
                                   email="a_" + self.email,
                                   password=self.password)
        create_user(username="b_" + self.username, email="b_" + self.email,
                    password=self.password, user_type=UserType.ADMIN)

        user_list = get_users(UserType.CANDIDATE)

        self.assertEqual(user_list.count(), 1)
        self.assertEqual(user_list[0]['_id'], create_user1['_id'])
        self.assertFalse('password' in user_list[0])

    def test_get_user(self):
        create_user(username=self.username, email=self.email,
                    password=self.password)

        user = get_user(self.username)

        self.assertEqual(user['email'], self.email)
        self.assertTrue(check_password(self.password, user['password']))

    def test_get_user_that_does_not_exists(self):
        create_user(username=self.username, email=self.email,
                    password=self.password)

        user = get_user(self.username + "something")

        self.assertIsNone(user)

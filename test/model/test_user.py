from db.collections import users
from lib.password import check_password
from model.user import create_user, UserType, get_users, get_user
from test import UnitTestCase


class UserTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.email = "email@one.it"
        self.password = "some_password"

    def tearDown(self):
        super().tearDown()
        users.drop()

    def test_create_user(self):
        create_user(email=self.email, password=self.password)

        user = users.find_one({'_id': self.email})
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], UserType.CANDIDATE)

    def test_create_admin_user(self):
        user_type = UserType.ADMIN
        create_user(email=self.email, password=self.password,
                    user_type=user_type)

        user = users.find_one({'_id': self.email})
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], user_type)

    def test_create_hiring_manager_user(self):
        user_type = UserType.HIRING_MANAGER
        create_user(email=self.email, password=self.password,
                    user_type=user_type)

        user = users.find_one({'_id': self.email})
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], user_type)

    def test_create_user_no_email_raises_value_error(self):

        with self.assertRaises(ValueError):
            create_user(email=None, password='some password')

        with self.assertRaises(ValueError):
            create_user(email='', password='some password')

    def test_create_user_no_password_raises_value_error(self):

        with self.assertRaises(ValueError):
            create_user(email='some@email.com', password=None)

        with self.assertRaises(ValueError):
            create_user(email='some@email.com', password='')

    def test_create_user_invalid_email(self):

        with self.assertRaises(ValueError):
            create_user(email='some_invalid_email', password="password")

    def test_create_users_with_same_emails(self):
        create_user(email=self.email, password=self.password)

        with self.assertRaises(ValueError):
            create_user(email=self.email, password=self.password)


class GetUserTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.email = "email@one.it"
        self.password = "some_password"

    def tearDown(self):
        super().tearDown()
        users.drop()

    def test_get_users(self):
        expected_email = "a_" + self.email
        create_user(email=expected_email, password=self.password)
        create_user(email="b_" + self.email, password=self.password,
                    user_type=UserType.ADMIN)

        user_list = get_users(UserType.CANDIDATE)

        self.assertEqual(user_list.count(), 1)
        self.assertEqual(user_list[0]['_id'], expected_email)
        self.assertFalse('password' in user_list[0])

    def test_get_user(self):
        create_user(email=self.email, password=self.password)

        user = get_user(self.email)

        self.assertEqual(user['_id'], self.email)
        self.assertTrue(check_password(self.password, user['password']))

    def test_get_user_that_does_not_exists(self):
        create_user(email=self.email, password=self.password)

        user = get_user(self.email + "something")

        self.assertIsNone(user)

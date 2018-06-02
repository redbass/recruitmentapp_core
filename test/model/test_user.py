from db.collections import users
from lib.password import check_password
from model.user import create_user, UserType
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
        self.assertTrue(check_password(user['password'], self.password))
        self.assertEqual(user['type'], UserType.CANDIDATE)

    def test_create_admin_user(self):
        user_type = UserType.ADMIN
        create_user(email=self.email, password=self.password,
                    user_type=user_type)

        user = users.find_one({'_id': self.email})
        self.assertEqual(user['password'], self.password)
        self.assertEqual(user['type'], user_type)

    def test_create_hiring_manager_user(self):
        user_type = UserType.HIRING_MANAGER
        create_user(email=self.email, password=self.password,
                    user_type=user_type)

        user = users.find_one({'_id': self.email})
        self.assertEqual(user['password'], self.password)
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

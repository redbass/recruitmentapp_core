from db.collections import users
from lib.password import check_password
from model.user import create_user, UserType
from test.model.user.test_user import BaseUserTestCase


class UserTestCase(BaseUserTestCase):

    def test_create_user(self):
        created_user = create_user(username='userNamE', email=self.email,
                                   password=self.password)

        user = users.find_one({'_id': created_user['_id']})
        self.assertTrue(self.email, user['email'])
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], UserType.CANDIDATE)

    def test_create_admin_user(self):
        user_type = UserType.ADMIN
        created_user = create_user(username='userNamE', email=self.email,
                                   password=self.password, user_type=user_type)

        user = users.find_one({'_id': created_user['_id']})
        self.assertTrue(self.email, user['email'])
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], user_type)

    def test_create_hiring_manager_user(self):
        user_type = UserType.HIRING_MANAGER
        created_user = create_user(username='userNamE', email=self.email,
                                   password=self.password, user_type=user_type)

        user = users.find_one({'_id': created_user['_id']})
        self.assertTrue(self.email, user['email'])
        self.assertTrue(check_password(self.password, user['password']))
        self.assertEqual(user['type'], user_type)

    def test_create_user_no_username_raises_value_error(self):

        with self.assertRaises(ValueError):
            create_user(username=None, email=None, password='some password')

        with self.assertRaises(ValueError):
            create_user(username='', email='', password='some password')

    def test_create_user_no_email_raises_value_error(self):

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email=None,
                        password='some password')

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email='',
                        password='some password')

    def test_create_user_no_password_raises_value_error(self):

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email='some@email.com',
                        password=None)

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email='some@email.com',
                        password='')

    def test_create_user_with_same_username(self):

        create_user(username='userNamE', email='some@email.com',
                    password="password")

        with self.assertRaisesRegex(
                ValueError, 'Username `.*` has already been used'):
            create_user(username='userNamE', email='some@email.com',
                        password="password")

    def test_create_user_invalid_email(self):

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email='some_invalid_email',
                        password="password")

    def test_create_users_with_same_emails(self):
        create_user(username='userNamE', email=self.email,
                    password=self.password)

        with self.assertRaises(ValueError):
            create_user(username='userNamE', email=self.email,
                        password=self.password)

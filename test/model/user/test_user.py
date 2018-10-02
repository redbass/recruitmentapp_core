from lib.password import check_password
from model.user import UserType, get_user, get_users
from test import UnitTestCase
from test.model.user import UserFactory


class BaseUserTestCase(UnitTestCase):
    pass


class CreateUserTestCase(BaseUserTestCase):

    def setUp(self):
        super().setUp()
        self.username = "test@email.com"
        self.password = "password"
        self.first_name = "My"
        self.last_name = "Name"
        self.title = "Mr"
        self.user_type = UserType.ADMIN

    def test_create(self):
        stored_user = self.create_from_factory(
            UserFactory,
            username=self.username, password=self.password,
            title=self.title, first_name=self.first_name,
            last_name=self.last_name, user_type=self.user_type)

        self.assertTrue(check_password(self.password,
                                       stored_user.pop('password')))

        self.assertEquals({
            '_id': self.username,
            'type': self.user_type,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title
        }, stored_user)

    def test_create_unique_user(self):
        self.create_from_factory(UserFactory, username="io@io.it")

        with self.assertRaisesRegex(ValueError,
                                    "A user with this email already exists"):
            self.create_from_factory(UserFactory, username="io@io.it")

    def test_create_with_invalid_email_raises_exception(self):
        with self.assertRaises(ValueError):
            self.create_from_factory(UserFactory,
                                     username="some_invalid_email")


class GetUserTestCase(BaseUserTestCase):

    def test_get_users(self):
        user_type = UserType.CANDIDATE
        created_user1 = self.create_from_factory(UserFactory,
                                                 user_type=user_type)
        self.create_from_factory(UserFactory)

        user_list = get_users(user_type)

        self.assertEqual(user_list.count(), 1)
        self.assertEqual(user_list[0]['_id'], created_user1['_id'])

    def test_get_users_no_password(self):
        user_type = UserType.CANDIDATE
        self.create_from_factory(UserFactory, user_type=user_type)
        self.create_from_factory(UserFactory, user_type=user_type)

        user_list = get_users(user_type, exclude_password=True)
        for user in user_list:
            self.assertIsNone(user.get('password'))
            self.assertIsNotNone(user.get('first_name'))

    def test_get_user(self):
        created_user = self.create_from_factory(UserFactory)
        self.create_from_factory(UserFactory)

        user = get_user(created_user['_id'])

        self.assertEquals(created_user['_id'], user['_id'])

    def test_get_user_no_password(self):
        created_user = self.create_from_factory(UserFactory)
        self.create_from_factory(UserFactory)

        user = get_user(created_user['_id'], exclude_password=True)

        self.assertIsNone(user.get('password'))
        self.assertIsNotNone(user.get('first_name'))

    def test_get_user_that_does_not_exists(self):
        self.create_from_factory(UserFactory)

        user = get_user("something")

        self.assertIsNone(user)

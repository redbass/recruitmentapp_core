from lib.password import check_user_password
from model.user import UserType, get_user, get_users, \
    create_hidden_hiring_manager, update_user_password
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

        self.assertTrue(check_user_password(self.password,
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

    def test_create_hidden_hiring_manager(self):
        create_hidden_hiring_manager(username=self.username)
        stored_user = get_user(username=self.username)

        self.assertEquals(stored_user['_id'], self.username)
        self.assertIsNotNone(stored_user['password'], self.username)
        self.assertEquals(stored_user['type'], UserType.HIRING_MANAGER)
        self.assertEquals(stored_user['first_name'], self.username)
        self.assertEquals(stored_user['last_name'], self.username)
        self.assertIsNone(stored_user['title'])


class GetUserTestCase(BaseUserTestCase):

    def test_get_users(self):
        expected_users = self._create_some_users()
        expected_ids = [u['_id'] for u in expected_users]

        result_users = get_users()

        result_ids = [u['_id'] for u in result_users]
        self.assertEqual(expected_ids, result_ids)

    def test_get_users_exclude_password(self):
        expected_users = self._create_some_users()
        expected_ids = [u['_id'] for u in expected_users]

        result_users = get_users(exclude_password=True)

        result_ids = [u['_id'] for u in result_users]
        self.assertEqual(expected_ids, result_ids)
        for user in result_users:
            self.assertIsNone(user.get('password'))

    def test_get_users_by_type(self):
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

    def _create_some_users(self):
        user_1 = self.create_from_factory(
            UserFactory, user_type=UserType.ADMIN)
        user_2 = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)
        user_3 = self.create_from_factory(
            UserFactory, user_type=UserType.ADMIN)
        user_4 = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)
        expected_users = [user_1, user_2, user_3, user_4]
        return expected_users


class UpdateUserPasswordTestCase(BaseUserTestCase):

    def test_set_password(self):
        user = self.create_from_factory(UserFactory)

        new_password = "new_password"

        update_user_password(user_id=user['_id'], new_password=new_password)

        stored_user = get_user(username=user['_id'])

        self.assertTrue(check_user_password(new_password,
                                            stored_user['password']))

    def test_set_password_invalid_id(self):

        new_password = "new_password"

        with self.assertRaises(ValueError):
            update_user_password(user_id='123', new_password=new_password)

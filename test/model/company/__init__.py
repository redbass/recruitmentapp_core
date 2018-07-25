from db.collections import companies, users
from model.user import create_user, UserType
from test import UnitTestCase


class BaseTestCompany(UnitTestCase):

    def setUp(self):
        super().setUp()

        self.hiring_manager1 = create_user(username='hiring_manager1',
                                           email="hiring_manager1@g.mail",
                                           password='test',
                                           user_type=UserType.HIRING_MANAGER)

        self.hiring_manager2 = create_user(username='hiring_manager2',
                                           email="hiring_manager2@g.mail",
                                           password='test',
                                           user_type=UserType.HIRING_MANAGER)

    def tearDown(self):
        super().tearDown()
        companies.drop()
        users.drop()

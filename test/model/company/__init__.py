from db.collections import companies, users
from model.user import create_user, UserType
from test import UnitTestCase


class BaseTestCompany(UnitTestCase):

    def setUp(self):
        super().setUp()

        self.hiring_manager = create_user(username='test1',
                                          email="test1@g.mail",
                                          password='test',
                                          user_type=UserType.HIRING_MANAGER)

    def tearDown(self):
        super().tearDown()
        companies.drop()
        users.drop()

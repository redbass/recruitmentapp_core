from db.collections import users, companies, jobs
from model.company.company import create_company
from model.user import create_user, UserType
from test import UnitTestCase


class BaseTestJob(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.admin_user = create_user(username='admin_user',
                                      email='email@posta.it',
                                      password='password',
                                      user_type=UserType.ADMIN)
        self.company = create_company(admin_user_id=self.admin_user['_id'],
                                      name='Company Name',
                                      description='some Description')

    def tearDown(self):
        super().tearDown()
        users.drop()
        companies.drop()
        jobs.drop()

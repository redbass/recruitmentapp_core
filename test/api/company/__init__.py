from db.collections import users, companies
from test.api import TestApi


class BaseTestCompany(TestApi):

    def tearDown(self):
        users.drop()
        companies.drop()
        super().tearDown()

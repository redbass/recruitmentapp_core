from db.collections import companies, users
from model.company.company import create_company
from model.user import UserType
from test import UnitTestCase, load_example_model
from test.factory import ModelFactory
from test.model.user import UserFactory


class BaseTestCompany(UnitTestCase):

    def setUp(self):
        super().setUp()

        self.hiring_manager1 = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)

        self.hiring_manager2 = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)

    def tearDown(self):
        companies.drop()
        users.drop()
        super().tearDown()


class CompanyFactory(ModelFactory):
    EXAMPLE_MODEL_NAME = 'create_company_input'

    def create(self, **qwargs):

        default_values = load_example_model(self.EXAMPLE_MODEL_NAME)

        if 'admin_user_ids' not in qwargs:
            user = self.create_from_factory(UserFactory)
            default_values['admin_user_ids'] = [user['_id']]

        default_values.update(qwargs)

        return create_company(**default_values)

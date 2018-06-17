from db.collections import companies, users
from model.user import create_user, UserType
from test import UnitTestCase
from model.company import create_company, get_company, get_companies, \
    get_company_by_admin_user


class BaseTestCompay(UnitTestCase):

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


class TestCreateCompany(BaseTestCompay):

    def test_create_company_as_admin(self):
        admin = create_user(username='test2',
                            email="test2@g.mail",
                            password='test',
                            user_type=UserType.ADMIN)
        expected_company = {
            '_id': '1',
            'name': 'ACME Inc.',
            'description': 'some description',
            'admin_user_ids': [admin['_id']],
            'hire_managers_ids': []
        }

        company = create_company(name=expected_company['name'],
                                 admin_user_id=admin['_id'],
                                 description=expected_company['description'])

        created_company = get_company(company['_id'])

        expected_company.pop('_id')

        self.assertIsNotNone(created_company.pop('_id'))
        self.assertEqual(expected_company, created_company)

    def test_create_company_as_hiring_manager(self):
        expected_company = {
            '_id': '1',
            'name': 'ACME Inc.',
            'description': 'some description',
            'admin_user_ids': [self.hiring_manager['_id']],
            'hire_managers_ids': []
        }

        company = create_company(name=expected_company['name'],
                                 admin_user_id=self.hiring_manager['_id'],
                                 description=expected_company['description'])

        created_company = get_company(company['_id'])

        expected_company.pop('_id')

        self.assertIsNotNone(created_company.pop('_id'))
        self.assertEqual(expected_company, created_company)

    def test_create_company_without_name_raise_error(self):
        with self.assertRaisesRegex(ValueError,
                                    "Company `name` is a required field"):
            create_company(name="", admin_user_id="1")

    def test_create_company_with_invalid_user_id_raise_error(self):
        with self.assertRaisesRegex(ValueError,
                                    "The given user admin id `.*` is not "
                                    "valid"):
            create_company(name="random", admin_user_id="1")

    def test_create_company_with_invalid_user_type_raise_error(self):
        user = create_user(username='test', email="test@g.mail",
                           password='test')
        with self.assertRaisesRegex(ValueError,
                                    "The given user admin id `.*` is not a "
                                    "`hiring manager` or an `admin`"):
            create_company(name="random", admin_user_id=user['_id'])

    def test_create_company_with_same_admin_user_raises_error(self):
        create_company(name="random", admin_user_id=self.hiring_manager['_id'])

        with self.assertRaisesRegex(ValueError,
                                    "A company with the same "
                                    "admin user `.*` already exists"):
            create_company(name="random",
                           admin_user_id=self.hiring_manager['_id'])


class TestGetCompanies(BaseTestCompay):

    def test_get_companies(self):
        user2 = create_user(username='test2',
                            email="test2@g.mail",
                            password='test',
                            user_type=UserType.HIRING_MANAGER)

        company_1 = create_company(name="c1",
                                   admin_user_id=self.hiring_manager['_id'])
        company_2 = create_company(name="c2",
                                   admin_user_id=user2['_id'])

        result = get_companies()

        self.assertEqual(list(result), [company_1, company_2])


class TestGetCompanyById(BaseTestCompay):

    def setUp(self):
        super().setUp()

        self.company_1 = create_company(
            name="c1", admin_user_id=self.hiring_manager['_id'])

    def test_get_company_by_admin_user(self):
        stored_company1 = get_company_by_admin_user(self.hiring_manager['_id'])
        self.assertEqual(self.company_1, stored_company1)

    def test_no_result_returned_if_no_company(self):
        stored_company = get_company_by_admin_user("random")
        self.assertIsNone(stored_company)

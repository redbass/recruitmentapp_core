from model.company.company import create_company, get_company
from model.user import create_user, UserType
from test.model.company import BaseTestCompany


class TestCreateCompany(BaseTestCompany):

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
            'admin_user_ids': [self.hiring_manager1['_id']],
            'hire_managers_ids': []
        }

        company = create_company(name=expected_company['name'],
                                 admin_user_id=self.hiring_manager1['_id'],
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
        create_company(name="random",
                       admin_user_id=self.hiring_manager1['_id'])

        with self.assertRaisesRegex(ValueError,
                                    "A company with the same "
                                    "admin user `.*` already exists"):
            create_company(name="random",
                           admin_user_id=self.hiring_manager1['_id'])

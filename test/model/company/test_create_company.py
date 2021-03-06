from model.company.company import get_company, \
    _validate_admin_id, create_company_admin, create_company_hiring_manager
from model.user import UserType
from test import load_example_model
from test.model.company import BaseTestCompany
from test.model.test_user import UserFactory


class TestCreateCompany(BaseTestCompany):

    def setUp(self):
        super().setUp()
        self.admin = self.create_from_factory(UserFactory,
                                              user_type=UserType.ADMIN)

    def test_create_company_as_admin_add_hidden_hiring_manager_user(self):
        self._assert_create_company(self.admin, is_admin=True,
                                    create_fn=create_company_admin)

    def test_create_company_as_hiring_manager(self):
        self._assert_create_company(self.hiring_manager1,
                                    create_fn=create_company_hiring_manager)

    def test_validate_admin_id_with_invalid_user_id_raise_error(self):
        with self.assertRaisesRegex(ValueError,
                                    "The given user admin id `.*` is not "
                                    "valid"):
            _validate_admin_id(admin_user_id="1")

    def test_create_company_with_invalid_user_type_raise_error(self):
        user = self.create_from_factory(UserFactory,
                                        user_type=UserType.CANDIDATE)
        with self.assertRaisesRegex(ValueError,
                                    "The given user admin id `.*` is not a "
                                    "`hiring manager` or an `admin`"):
            _validate_admin_id(admin_user_id=user['_id'])

    def test_create_company_with_same_admin_user_raises_error(self):
        self._assert_create_company(user=self.hiring_manager1,
                                    create_fn=create_company_hiring_manager)

        with self.assertRaisesRegex(ValueError,
                                    "A company with the same "
                                    "admin user `.*` already exists"):
            _validate_admin_id(admin_user_id=self.hiring_manager1['_id'])

    def _assert_create_company(self, user, create_fn, is_admin=False):
        create_company_input = load_example_model('create_company_input')
        company = create_fn(admin_user_id=user['_id'],
                            **create_company_input)
        expected_ids = [user['_id'], company['contacts']['email']] \
            if is_admin else [user['_id']]
        expected_company = {
            '_id': company['_id'],
            'hire_managers_ids': expected_ids,
            'admin_user_ids': expected_ids
        }
        expected_company.update(create_company_input)
        expected_company['enabled'] = is_admin
        created_company = get_company(company['_id'])
        self.assertIsNotNone(created_company['_id'])
        self.assertEqual(expected_company, created_company)
        return created_company

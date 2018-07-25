from model.user import create_user, UserType
from model.company.company import create_company, get_companies, \
    get_company_by_admin_user
from test.model.company import BaseTestCompany


class TestGetCompanies(BaseTestCompany):

    def setUp(self):
        super().setUp()
        user = create_user(username='user',
                           email="user@g.mail",
                           password='user',
                           user_type=UserType.HIRING_MANAGER)

        self.company_1 = create_company(
            name="c1", admin_user_id=self.hiring_manager1['_id'])
        self.company_2 = create_company(
            name="c2", admin_user_id=user['_id'])
        self.company_3 = create_company(
            name="c3", admin_user_id=self.hiring_manager2['_id'])

    def test_get_companies(self):
        result = get_companies()
        self.assertEqual(
            [self.company_1, self.company_2, self.company_3], list(result))

    def test_get_companies_by_id(self):
        expected_ids = [self.company_1['_id'], self.company_3['_id']]
        result = get_companies(expected_ids)

        result_ids = [r['_id'] for r in result]
        self.assertEqual(sorted(expected_ids), sorted(result_ids))


class TestGetCompanyById(BaseTestCompany):

    def setUp(self):
        super().setUp()

        self.company_1 = create_company(
            name="c1", admin_user_id=self.hiring_manager1['_id'])

    def test_get_company_by_admin_user(self):
        stored_company1 = get_company_by_admin_user(
            self.hiring_manager1['_id'])
        self.assertEqual(self.company_1, stored_company1)

    def test_no_result_returned_if_no_company(self):
        stored_company = get_company_by_admin_user("random")
        self.assertIsNone(stored_company)

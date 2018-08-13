from model.company.company import get_companies, \
    get_company_by_admin_user
from model.user import UserType
from test.model.company import BaseTestCompany, CompanyFactory
from test.model.user import UserFactory


class TestGetCompanies(BaseTestCompany):

    def setUp(self):
        super().setUp()
        user = self.create_from_factory(
            UserFactory, user_type=UserType.HIRING_MANAGER)

        self.company_1 = self.create_from_factory(
            CompanyFactory, admin_user_ids=[self.hiring_manager1['_id']])
        self.company_2 = self.create_from_factory(
            CompanyFactory, admin_user_ids=[user['_id']])
        self.company_3 = self.create_from_factory(
            CompanyFactory, admin_user_ids=[self.hiring_manager2['_id']])

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

        self.company_1 = self.create_from_factory(
            CompanyFactory, admin_user_ids=[self.hiring_manager1['_id']])

    def test_get_company_by_admin_user(self):
        stored_company1 = get_company_by_admin_user(
            self.hiring_manager1['_id'])
        self.assertEqual(self.company_1, stored_company1)

    def test_no_result_returned_if_no_company(self):
        stored_company = get_company_by_admin_user("random")
        self.assertIsNone(stored_company)

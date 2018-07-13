from model.user import create_user, UserType
from model.company.company import create_company, get_companies, \
    get_company_by_admin_user
from test.model.company import BaseTestCompany


class TestGetCompanies(BaseTestCompany):

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


class TestGetCompanyById(BaseTestCompany):

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

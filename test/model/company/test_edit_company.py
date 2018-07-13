from model.company.company import create_company, get_company
from model.company.edit_company import edit_company
from test.model.company import BaseTestCompany


class TestEditCompany(BaseTestCompany):

    def setUp(self):
        super().setUp()

        self.company = create_company(
            name="old name", description="old description",
            admin_user_id=self.hiring_manager['_id'])

    def test_edit_company(self):
        new_name = "new name"
        new_description = "new description"
        company_id = self.company['_id']

        edit_company(company_id=company_id, new_name=new_name,
                     new_description=new_description)

        updated_company = get_company(company_id=company_id)

        self.assertEqual(new_name, updated_company['name'])
        self.assertEqual(new_description, updated_company['description'])

    def test_edit_company_partially(self):
        new_description = "new description"
        company_id = self.company['_id']

        edit_company(company_id=company_id, new_description=new_description)

        updated_company = get_company(company_id=company_id)

        self.assertEqual(self.company['name'], updated_company['name'])
        self.assertEqual(new_description, updated_company['description'])

    def test_cannot_update_name_to_null(self):
        company_id = self.company['_id']

        with self.assertRaisesRegex(
                ValueError, 'Company name and description are required'):
            edit_company(company_id=company_id, new_name="new name",
                         new_description=None)

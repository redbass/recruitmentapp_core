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

    def test_cannot_update_name_to_null_or_empty_string(self):
        company_id = self.company['_id']

        with self.assertRaisesRegex(
                ValueError, 'Company name and description cannot be null '
                            'or empty string'):
            edit_company(company_id=company_id, new_name=None,
                         new_description="New Description")

        with self.assertRaisesRegex(
                ValueError, 'Company name and description cannot be null '
                            'or empty string'):
            edit_company(company_id=company_id, new_name="",
                         new_description="New Description")

    def test_cannot_update_description_to_null_or_empty_string(self):
        company_id = self.company['_id']

        with self.assertRaisesRegex(
                ValueError, 'Company name and description cannot be null '
                            'or empty string'):
            edit_company(company_id=company_id, new_name="new name",
                         new_description=None)

        with self.assertRaisesRegex(
                ValueError, 'Company name and description cannot be null '
                            'or empty string'):
            edit_company(company_id=company_id, new_name="new name",
                         new_description="")

    def test_company_id_does_not_exists(self):

        company_id = "SOMETHING"
        with self.assertRaisesRegex(
                ValueError, 'Company id "{company_id}" does not exists'
                .format(company_id=company_id)):

            edit_company(company_id=company_id, new_name="New Name")

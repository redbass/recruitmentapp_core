from model.company.company import get_company
from model.company.edit_company import edit_company, enable_company, \
    disable_company
from test.model.company import BaseTestCompany, CompanyFactory


class TestEditCompany(BaseTestCompany):

    def setUp(self):
        super().setUp()

        self.company = self.create_from_factory(
            CompanyFactory,
            name="old name", description="old description",
            admin_user_ids=[self.hiring_manager1['_id']])

    def test_edit_company(self):
        new_values = {
            "name": "The New Name",
            "contacts": {
                "address": {
                    "number": "The new number"
                }
            }
        }

        edited_company = edit_company(_id=self.company['_id'], **new_values)

        self.assertEqual(new_values['name'],
                         edited_company['name'])
        self.assertEqual(new_values['contacts']['address']['number'],
                         edited_company['contacts']['address']['number'])

        self.assertEqual(self.company['description'],
                         edited_company['description'])
        self.assertEqual(self.company['contacts']['address']['street'],
                         edited_company['contacts']['address']['street'])

    def test_company_id_does_not_exists(self):
        company_id = "SOMETHING"
        with self.assertRaisesRegex(
                ValueError,
                'Company id "{company_id}" does not exists'.format(
                    company_id=company_id)):
            edit_company(_id=company_id, name="New Name")

    def test_enable_disable_company(self):
        enable_company(_id=self.company['_id'])
        company = get_company(self.company['_id'])
        self.assertTrue(company['enabled'])

        disable_company(_id=self.company['_id'])
        company = get_company(self.company['_id'])
        self.assertFalse(company['enabled'])

        enable_company(_id=self.company['_id'])
        company = get_company(self.company['_id'])
        self.assertTrue(company['enabled'])

from io import BytesIO

from db import get_grid_fs
from model.company.company import store_company_logo, get_company_logo
from test.model.company import BaseTestCompany, CompanyFactory


class TestCompanyLogo(BaseTestCompany):

    def setUp(self):
        super().setUp()
        self.grid_fs = get_grid_fs()
        self.company = self.create_from_factory(CompanyFactory)

    def test_can_store_file_by_company(self):
        logo_file = BytesIO("This is a logo".encode('utf-8'))
        store_company_logo(company_id=self.company['_id'],
                           file=logo_file)

        stored_logo = self.grid_fs.find_one({
            "company_id": self.company['_id']
        })

        logo_file.seek(0)
        self.assertEquals(logo_file.read(), stored_logo.read())

    def test_get_company_logo(self):
        logo_file = BytesIO("This is a logo".encode('utf-8'))
        store_company_logo(company_id=self.company['_id'],
                           file=logo_file)

        stored_logo = get_company_logo(self.company['_id'])

        logo_file.seek(0)
        self.assertEquals(logo_file.read(), stored_logo.read())

    def test_get_company_logo_returns_last_uploaded_logo(self):
        expected_logo_content = "This is a logo 3"
        self._store_logo("This is a logo 1")
        self._store_logo("This is a logo 2")
        self._store_logo(expected_logo_content)

        stored_logo = get_company_logo(self.company['_id'])

        self.assertEquals(expected_logo_content.encode('utf-8'),
                          stored_logo.read())

    def _store_logo(self, content):
        logo_file = BytesIO(content.encode('utf-8'))
        store_company_logo(company_id=self.company['_id'], file=logo_file)

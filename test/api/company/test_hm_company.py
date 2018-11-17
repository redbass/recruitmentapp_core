from json import loads

from api.routes.routes import COMPANIES_URL
from model.user import get_user, UserType
from test import load_example_model
from test.api.company import BaseTestCompany


class TestHMCompany(BaseTestCompany):

    def test_sign_in_company(self):

        data = load_example_model('sign_in_company')

        url = self.url_for(COMPANIES_URL)
        response = self.post_json(url, data)

        self.assertEqual(200, response.status_code)

        result_company = loads(response.data)
        stored_user_id = result_company['admin_user_ids'][0]

        self.assertEqual(data['company_name'], result_company['name'])
        self.assertEqual(data['company_description'],
                         result_company['description'])

        stored_user = get_user(stored_user_id)
        self.assertIsNotNone(stored_user)
        self.assertEqual(stored_user['type'], UserType.HIRING_MANAGER)

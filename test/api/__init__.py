import json

from flask import Response
from flask_jwt_extended import create_access_token

from api.routes.admin_routes import ADMIN_PREFIX
from app import get_app
from auth.jwt import _create_identity_object
from db.collections import setup_database
from model.user import UserType
from test import UnitTestCase
from test.model.company import CompanyFactory
from test.model.user import UserFactory

TEST_USER = 'test@user.com'


class TestApi(UnitTestCase):

    def setUp(self):
        super().setUp()
        setup_database()
        self.test_app = get_app().test_client()
        self._user, self._company = self._create_test_user()

    def _create_test_user(self):
        user = self.create_from_factory(UserFactory,
                                        user_type=UserType.ADMIN,
                                        username=TEST_USER)
        company = self.create_from_factory(CompanyFactory,
                                           admin_user_ids=[user['_id']])
        return user, company

    @staticmethod
    def url_for_admin(endpoint_url, **url_args):
        url = "/{prefix}{url}".format(prefix=ADMIN_PREFIX, url=endpoint_url)
        return TestApi.url_for(url, **url_args)

    @staticmethod
    def url_for(endpoint_url, **url_args):
        for key, val in url_args.items():
            endpoint_url = endpoint_url.replace('<{key}>'.format(key=key),
                                                str(val))
        return endpoint_url

    def get_data(self, url):
        self._create_headers()
        return self.test_app.get(url, headers=self._create_headers())

    def post_data(self, url, data=None, content_type=None, **qwargs):

        return self.test_app.post(url,
                                  headers=self._create_headers(),
                                  data=data,
                                  content_type=content_type,
                                  **qwargs)

    def post_json(self, url, data=None):
        return self.post_data(url, data=json.dumps(data or {}),
                              content_type='application/json')

    def assert_error(self,
                     response: Response,
                     error_status: int,
                     error_message: str):
        self.assertEqual(error_status, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(data['message'], error_message)

    def _create_headers(self):
        with get_app().test_request_context():
            identity = _create_identity_object(self._user)
            token = create_access_token(identity)
            return {
                'Authorization': 'Bearer {}'.format(token)
            }

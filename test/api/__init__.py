import json

from flask import Response

from app import get_app
from test import UnitTestCase


class TestApi(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.test_app = get_app().test_client()

    @staticmethod
    def url_for(endpoint_url, **url_args):
        for key, val in url_args.items():
            endpoint_url = endpoint_url.replace('<{key}>'.format(key=key),
                                                str(val))
        return endpoint_url

    def get_json(self, url):
        return self.test_app.get(url)

    def post_json(self, url, data={}):
        return self.test_app.post(url,
                                  data=json.dumps(data),
                                  content_type='application/json')

    def assert_error(self,
                     response: Response,
                     error_status: int,
                     error_message: str):
        self.assertEqual(error_status, response.status_code)
        data = json.loads(response.data)
        self.assertEqual(data['message'], error_message)

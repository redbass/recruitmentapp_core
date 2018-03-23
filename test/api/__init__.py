import json
from unittest import TestCase

from app import app


class TestApi(TestCase):

    def setUp(self):
        self.test_app = app.test_client()

    @staticmethod
    def url_for(endpoint_url, **url_args):
        for key, val in url_args.items():
            endpoint_url = endpoint_url.replace('<{key}>'.format(key=key), val)
        return endpoint_url

    def get_json(self, url):
        return self.test_app.get(url)

    def post_json(self, url, data):
        return self.test_app.post(url,
                                  data=json.dumps(data),
                                  content_type='application/json')

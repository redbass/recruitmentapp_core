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

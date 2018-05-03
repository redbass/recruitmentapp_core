import json
from unittest import TestCase

from app import get_app
from config import settings


class IntegrationTestCase(TestCase):

    def setUp(self):
        if not settings.TEST_MODE:
            raise Exception('Test have to run in test mode')

        self.test_app = get_app().test_client()

    def post_json(self, url, data):
        return self.test_app.post(url,
                                  data=json.dumps(data),
                                  content_type='application/json')

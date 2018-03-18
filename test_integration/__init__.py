from unittest import TestCase

from config import get_config


class IntegrationTestCase(TestCase):

    def setUp(self):
        if get_config().TEST_MODE:
            raise Exception('Test have to run in test mode')

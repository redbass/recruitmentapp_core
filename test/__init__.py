from unittest import TestCase

from config import settings


class UnitTestCase(TestCase):

    def setUp(self):
        if not settings.TEST_MODE:
            raise Exception('Test have to run in test mode')

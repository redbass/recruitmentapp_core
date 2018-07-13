from json import load
from unittest import TestCase

import pkg_resources

from config import settings
from db import get_db_name
from db.collections import db


class UnitTestCase(TestCase):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        db_name = get_db_name()
        db.client.drop_database(db_name)

    def setUp(self):
        if not settings.TEST_MODE:
            raise Exception('Test have to run in test mode')

    @staticmethod
    def load_fixture(file_name: str) -> dict:
        path = pkg_resources.resource_filename(
            'resources', 'fixtures/' + file_name + '.json')
        with open(path, 'r') as f:
            return load(f)

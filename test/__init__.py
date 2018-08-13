from json import load, loads
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
        try:
            db.client.drop_database(db_name)
        except AttributeError:
            pass

    def setUp(self):
        if not settings.TEST_MODE:
            raise Exception('Test have to run in test mode')

    @staticmethod
    def load_fixture(file_name: str) -> dict:
        path = pkg_resources.resource_filename(
            'resources', 'fixtures/' + file_name + '.json')
        with open(path, 'r') as f:
            return load(f)

    @classmethod
    def create_from_factory(cls, factory, **qwargs):
        return factory().create(**qwargs)


def load_example_model(model_name):
    file_name = 'example_models/{name}.json'.format(name=model_name)
    model = pkg_resources.resource_string('resources', file_name)
    return loads(model)

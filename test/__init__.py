import logging
from json import loads
from unittest import TestCase

import pkg_resources

from config import settings
from db import get_db_name
from db.collections import db, companies, users, jobs, payments, applications
from lib.schema_validation import validate

logging.getLogger('faker.factory').setLevel(logging.ERROR)


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

    def tearDown(self):
        companies.drop()
        users.drop()
        jobs.drop()
        payments.drop()
        applications.drop()
        super().tearDown()

    @classmethod
    def create_from_factory(cls, factory, **qwargs):
        return factory().create(**qwargs)

    @staticmethod
    def assert_validate_json_schema(json_schema_name, data):
        try:
            validate(json_schema_name, data)
        except Exception as e:
            assert False, "The provided data is not a valid `{schema}`: {msg}"\
                .format(schema=json_schema_name, msg=str(e))

    @staticmethod
    def load_example_model(model_name):
        file_name = 'example_models/{name}.json'.format(name=model_name)
        model = pkg_resources.resource_string('resources', file_name)
        return loads(model)


load_example_model = UnitTestCase.load_example_model

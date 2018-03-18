from json import loads
from unittest import TestCase

from api.handler import json_response


class TestHandler(TestCase):

    def test_json_response(self):
        _test_foo_data = {
            "test": "data"
        }

        @json_response
        def _test_foo():
            return _test_foo_data

        result, code = _test_foo()
        self.assertEqual(loads(result), _test_foo_data)
        self.assertEqual(code, 200)


class TestErrorHandler(TestCase):

    def test_json_response_error(self):
        err_msg = "Random exception"

        _test_foo_error_data = {
            "error": 'Unexpected error',
            "exception": err_msg
        }

        @json_response
        def _test_foo():
            raise Exception("Random exception")

        result, code = _test_foo()
        self.assertEqual(loads(result), _test_foo_error_data)
        self.assertEqual(code, 500)

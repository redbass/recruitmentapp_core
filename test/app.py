from unittest import TestCase

from flask import Flask


class TestGetApp(TestCase):

    def test_return_flask_app(self):
        from app import get_app

        result = get_app()
        self.assertEqual(type(result), Flask)

    def test_is_a_singleton(self):
        from app import get_app

        first_result = get_app()
        second_result = get_app()

        self.assertEqual(first_result, second_result)



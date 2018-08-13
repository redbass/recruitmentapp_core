from unittest import TestCase

from db.utils import dict_to_datapath


class TestWalker(TestCase):

    def test_walker_base_case(self):

        input = {'a': 1}
        expected = {'a': 1}

        result = dict_to_datapath(input)

        self.assertEqual(expected, result)

    def test_walker_base_case_2(self):

        input = {'a': 1, 'b': 1, 'c': None}
        expected = {'a': 1, 'b': 1, 'c': None}

        result = dict_to_datapath(input)

        self.assertEqual(expected, result)

    def test_dict_to_datapath_nested_once(self):
        input = {
            "a": 1,
            "b": {
                "ba": "value"
            },
            "c": None
        }

        expected = {
            "a": 1,
            "b.ba": "value",
            "c": None
        }

        result = dict_to_datapath(input)

        self.assertEqual(expected, result)

    def test_dict_to_datapath_nested_twice(self):
        input = {
            "a": 1,
            "b": {
                "ba": "value",
                "bb": {
                    "bba": "value2",
                    "bbb": "value3"
                }
            },
            "c": None
        }

        expected = {
            "a": 1,
            "b.ba": "value",
            "b.bb.bba": "value2",
            "b.bb.bbb": "value3",
            "c": None
        }

        result = dict_to_datapath(input)

        self.assertEqual(expected, result)

    def test_dict_to_datapath_nested_twice_2(self):
        input = {
            "a": 1,
            "b": {
                "ba": "value",
                "bb": {
                    "bba": "value2",
                    "bbb": "value3"
                }
            },
            "c": {
                "ca": None
            }
        }

        expected = {
            "a": 1,
            "b.ba": "value",
            "b.bb.bba": "value2",
            "b.bb.bbb": "value3",
            "c.ca": None
        }

        result = dict_to_datapath(input)

        self.assertEqual(expected, result)

    def test_dict_to_datapath_empty_dict(self):
            input = {
                "a": {}
            }

            expected = {
                "a": {}
            }

            result = dict_to_datapath(input)

            self.assertEqual(expected, result)

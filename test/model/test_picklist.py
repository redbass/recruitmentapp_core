from model.picklist import store_piclikst, get_picklist
from test import UnitTestCase


class TestLocation(UnitTestCase):

    def test_store_picklist(self):

        picklist_type = 'duration'
        picklist_values = [
            {'key': 'value1', 'value': 'Value One'},
            {'key': 'value2', 'value': 'Value Two'},
            {'key': 'value3', 'value': 'Value Three'}
        ]

        store_piclikst(picklist_type, picklist_values)

        stored_picklist = get_picklist(picklist_type)

        self.assertEquals(picklist_values, stored_picklist)

    def test_store_empty_picklist_values_raise_error(self):
        picklist_values = []

        with self.assertRaises(ValueError):
            store_piclikst('duration', picklist_values)

    def test_store_invalid_picklist_values_raise_error(self):
        picklist_values = [
            ['value1', 'Value One'],
            ['value2', 'Value Two'],
            ['value3', 'Value Three']
        ]

        with self.assertRaises(ValueError):
            store_piclikst('duration', picklist_values)

    def test_store_invalid_picklist_values_raise_error_2(self):
        picklist_values = {}

        with self.assertRaises(ValueError):
            store_piclikst('duration', picklist_values)

    def test_store_invalid_picklist_raise_error(self):

        with self.assertRaises(ValueError):
            store_piclikst("random", {})

    def test_get_picklist_do_not_exists(self):
        self.assertIsNone(get_picklist('random'))

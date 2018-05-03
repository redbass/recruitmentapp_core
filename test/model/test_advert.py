from unittest.mock import patch

from model.advert import create_advert, delete_adverts, get_adverts, \
    get_all_adverts, DEFAULT_ADVERTS_PAGINATION_LIMIT, \
    DEFAULT_ADVERTS_PAGINATION_START
from model.location import Location
from test import UnitTestCase


class TestCreateAdvert(UnitTestCase):

    @patch('model.advert.create_id')
    @patch('model.advert.adverts')
    def test_create_advert(self, adverts, create_id):

        expected_id = '123'
        expected_title = 'title'
        expected_description = 'description'
        expected_advert = {
            '_id': expected_id,
            'title': expected_title,
            'description': expected_description,
            'period': {
                'start': None,
                'stop': None
            },
            'location': None,
            'draft': False,
            'deleted': False
        }

        create_id.return_value = expected_id

        created_advert = create_advert(
            title=expected_advert['title'],
            description=expected_advert['description']
        )

        self.assertEqual(created_advert, expected_advert)
        self.assertTrue(adverts.insert_one.called)

    def test_create_advert_parameters_error(self):
        self.assertRaises(AttributeError, create_advert, None, None)
        self.assertRaises(AttributeError, create_advert, '', '')
        self.assertRaises(AttributeError, create_advert, '123', None)
        self.assertRaises(AttributeError, create_advert, None, 'asd')

    @patch('model.advert.create_id')
    @patch('model.advert.adverts')
    def test_create_advert_with_location(self, _, create_id):
        expected_id = '123'
        location = Location(10, 20)
        created_advert = create_advert(location=location,
                                       title='test',
                                       description='test description')
        create_id.return_value = expected_id
        self.assertEqual(created_advert['location'],
                         location.get_geo_json_point())


class TestDeleteAdverts(UnitTestCase):

    @patch('model.advert.adverts')
    def test_delete_adverts(self, adverts):
        advert_to_delete_ids = ["123"]
        delete_adverts(advert_to_delete_ids)

        call_args = adverts.update_many.call_args[0]
        self.assertEqual(call_args[0], {'_id': {'$in': advert_to_delete_ids}})
        self.assertEqual(call_args[1], {'$set': {'deleted': True}})

    def test_delete_adverts_parameter_error(self):
        self.assertRaises(AttributeError, delete_adverts, None)
        self.assertRaises(AttributeError, delete_adverts, [])
        self.assertRaises(AttributeError, delete_adverts, '123')


class TestGetAdverts(UnitTestCase):

    @patch('model.advert.adverts')
    def test_get_adverts(self, adverts):
        _ids = ["123"]
        expected_advert = {}
        adverts.find.return_value = [expected_advert]

        result = get_adverts(_ids)

        self.assertEqual(result[0], expected_advert)

    def test_get_adverts_parameter_error(self):
        self.assertRaises(AttributeError, delete_adverts, None)
        self.assertRaises(AttributeError, delete_adverts, [])
        self.assertRaises(AttributeError, delete_adverts, '123')


class TestGetAllAdverts(UnitTestCase):

    @patch('model.advert.adverts')
    @patch('model.advert.get_pagination_from_cursor')
    def test_get_all_adverts(self, get_pagination, adverts):
        expected_adverts = "expected_adverts"
        expected_cursor = "cursor"

        expected_pagination_start = 2
        expected_pagination_limit = 20

        adverts.find.return_value = expected_cursor
        get_pagination.return_value = expected_adverts

        results = get_all_adverts(start=expected_pagination_start,
                                  limit=expected_pagination_limit)

        self.assertEqual(results, expected_adverts)
        adverts.find.assert_called_once_with({})
        get_pagination.assert_called_once_with(expected_cursor,
                                               expected_pagination_start,
                                               expected_pagination_limit)

    @patch('model.advert.adverts')
    @patch('model.advert.get_pagination_from_cursor')
    def test_get_all_adverts_null_params(self, get_pagination, adverts):
        expected_adverts = "expected_adverts"
        expected_cursor = "cursor"

        adverts.find.return_value = expected_cursor
        get_pagination.return_value = expected_adverts

        results = get_all_adverts(limit=None, start=None)

        self.assertEqual(results, expected_adverts)
        adverts.find.assert_called_once_with({})
        get_pagination.assert_called_once_with(
            expected_cursor,
            DEFAULT_ADVERTS_PAGINATION_START,
            DEFAULT_ADVERTS_PAGINATION_LIMIT)

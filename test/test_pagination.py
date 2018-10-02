from unittest.mock import MagicMock

from lib.pagination import get_pagination_from_cursor
from test import UnitTestCase


class TestCreateAdverts(UnitTestCase):

    def test_get_pagination_from_cursor(self):
        cursor = MagicMock()
        skip_mock = MagicMock()

        start = 0
        limit = 5
        expected_results = [1, 2, 3, 4, 5]
        expected_total = 5
        expected_pagination = {
            "start": start,
            "limit": limit,
            "total": expected_total,
            "hasNext": False,
            "results": expected_results
        }

        cursor.count.return_value = expected_total
        skip_mock.limit.return_value = expected_results
        cursor.skip.return_value = skip_mock

        result = get_pagination_from_cursor(cursor, start, limit)

        self.assertEqual(result, expected_pagination)
        cursor.skip.assert_called_once_with(start)
        skip_mock.limit.assert_called_once_with(limit)

    def test_get_pagination_from_cursor_has_more_results(self):
        cursor = MagicMock()
        start = 0
        limit = 2
        total_results = 10

        cursor.count.return_value = total_results

        pagination = get_pagination_from_cursor(cursor, start, limit)

        self.assertTrue(pagination['hasNext'])

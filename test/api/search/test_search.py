import json
from unittest.mock import patch

from api.routes.routes import SEARCH
from test.api import TestApi


class TestAPISearch(TestApi):

    @patch('api.search.jobs')
    def test_search(self, mock_jobs):
        query = "something"
        expected_results = [1, 2, 3]
        mock_jobs.search.return_value = expected_results

        url = SEARCH + "?query=" + query
        response = self.test_app.get(url)

        self.assertEqual(response.status_code, 200)

        results = json.loads(response.data)
        result_query = results['query']['string']
        result_jobs = results['jobs']

        self.assertEqual(query, result_query)
        self.assertEqual(expected_results, result_jobs)

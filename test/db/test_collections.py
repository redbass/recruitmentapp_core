from db.collections import jobs, setup_database
from test import UnitTestCase


class TestCollections(UnitTestCase):

    def test_job_search_index_created(self):
        setup_database()
        indexes = jobs.index_information()
        search_index = indexes.get('search_index')

        self.assertIsNotNone(search_index)
        self.assertEqual(2, len(search_index['key']))
        self.assertIn('title', search_index['weights'])
        self.assertIn('description', search_index['weights'])

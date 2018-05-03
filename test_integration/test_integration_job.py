from db.collections import adverts
from model.advert import create_advert, delete_adverts, get_adverts
from test_integration import IntegrationTestCase


class TestCreateAdvert(IntegrationTestCase):

    def tearDown(self):
        adverts.drop()

    def test_create_advert(self):
        title = 'The title'
        description = 'Advert Description!'

        expected_advert1 = create_advert(title + '1', description + '1')
        expected_advert2 = create_advert(title + '2', description + '2')

        created_advert1 = get_adverts([expected_advert1['_id']])
        created_advert2 = get_adverts([expected_advert2['_id']])

        self.assertEqual(created_advert1[0], expected_advert1)
        self.assertEqual(created_advert2[0], expected_advert2)

    def test_delete_advert(self):
        advert = create_advert('title', 'description')

        delete_adverts([advert['_id']])

        deleted_adverts = get_adverts([advert['_id']])
        self.assertTrue(deleted_adverts[0].get('deleted'))

from json import loads

from api.routes.routes import PICKLIST
from model.picklist import store_piclikst, get_picklist
from test.api import TestApi


class TestApiPicklist(TestApi):

    def test_get_picklist(self):

        expeceted_values = [
            {'key': 'key1', 'value': 'value1'},
            {'key': 'key2', 'value': 'value2'}
        ]
        picklist_type = 'job_titles'

        store_piclikst(picklist_type=picklist_type,
                       picklist_values=expeceted_values)

        url = self.url_for(PICKLIST, name=picklist_type)
        response = self.get_data(url)
        self.assertEqual(200, response.status_code)

        self.assertEquals(expeceted_values, loads(response.data))

    def test_store_picklist(self):

        expeceted_values = [
            {'key': 'key1', 'value': 'value1'},
            {'key': 'key2', 'value': 'value2'}
        ]
        picklist_type = 'job_titles'

        url = self.url_for(PICKLIST, name=picklist_type)
        response = self.post_json(url, data=expeceted_values)
        self.assertEqual(200, response.status_code)

        stored_values = get_picklist(picklist_type)

        self.assertEquals(expeceted_values, stored_values)

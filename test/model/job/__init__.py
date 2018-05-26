from db.collections import jobs
from test import UnitTestCase


class BaseTestJob(UnitTestCase):

    def tearDown(self):
        super().tearDown()
        jobs.drop()

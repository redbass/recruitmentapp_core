import json
from urllib.parse import urlencode

from api.routes.routes import SEARCH
from db.collections import create_indexes, users, companies, jobs
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    publish_job_advert
from test.api import TestApi
from test.model.job import JobFactory
from test.services.search import EDINBURGH_CENTER, EDINBURGH_ROSELIN_CHAPEL, \
    EDINBURGH_ARTHURS_SEAT, ITALY


class TestAPISearch(TestApi):

    def setUp(self):
        super().setUp()
        create_indexes()
        self.job_1 = self._crate_job(title="job 1",
                                     location=EDINBURGH_ROSELIN_CHAPEL)
        self.job_2 = self._crate_job(title="Something 2",
                                     location=EDINBURGH_ARTHURS_SEAT)
        self.job_3 = self._crate_job(title="job 3",
                                     location=ITALY)

    def tearDown(self):
        users.drop()
        companies.drop()
        jobs.drop()
        super().tearDown()

    def test_search(self):
        query = "job"
        location = [EDINBURGH_CENTER['latitude'],
                    EDINBURGH_CENTER['longitude']]
        location_str = ",".join([str(l) for l in location])
        radius = 5

        # TODO: This is wrong have to be fixed in the code
        expected_jobs = [self.job_1['title'], self.job_3['title']]
        expected_result_query = {
            "query": query,
            "location": location,
            "radius": float(radius)
        }

        params = urlencode({
            'query': query,
            'location': location_str,
            'radius': radius
        })

        url = "{root}?{params}".format(root=SEARCH, params=params)
        response = self.test_app.get(url)

        self.assertEqual(200, response.status_code)

        results = json.loads(response.data)
        jobs = results['jobs']
        result_query = results['query']

        self.assertEquals(expected_jobs, [j['title'] for j in jobs])
        self.assertEquals(expected_result_query, result_query)

    @classmethod
    def _crate_job(cls, **job_args):
        job = cls.create_from_factory(JobFactory, **job_args)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']

        approve_job_advert(job_id=job_id, advert_id=advert_id)
        publish_job_advert(job_id=job_id, advert_id=advert_id)

        return job

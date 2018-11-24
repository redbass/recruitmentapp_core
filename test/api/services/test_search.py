import json
from urllib.parse import urlencode

from api.routes.routes import SEARCH
from lib.geo import get_coordinates_from_location, distance_from_location
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    publish_job_advert, request_approval_job_advert
from test.api import TestApi
from test.model.job import JobFactory
from test.services.search import EDINBURGH_CENTER, EDINBURGH_ROSELIN_CHAPEL, \
    ITALY, STERLING_CASTLE


class TestAPISearch(TestApi):

    def setUp(self):
        super().setUp()
        self.current_location = EDINBURGH_CENTER
        self.job_type = "wizard"
        self.rate_type = "salary"
        self.job_1 = self._crate_job(title="job 1",
                                     location=EDINBURGH_ROSELIN_CHAPEL,
                                     metadata={'job_type': self.job_type},
                                     rate={'type': self.rate_type})
        self.job_2 = self._crate_job(title="Something 1",
                                     location=STERLING_CASTLE)
        self.job_3 = self._crate_job(title="job 3",
                                     location=ITALY)

    def test_search(self):
        query = "job"
        expected_jobs = [self.job_1]
        url_params = urlencode({
            'query': query,
            'job_type': self.job_type,
            'rate_type': self.rate_type,
        })
        self._assert_search(expected_jobs, url_params)

        self._assert_search(expected_jobs=expected_jobs, url_params=url_params)

    def test_search_distance_1(self):
        query = "job"
        expected_jobs = [self.job_1]
        job_location = STERLING_CASTLE

        self._assert_search_by_distance(job_location, query, expected_jobs,
                                        precision=1)

    def test_search_distance_2(self):
        query = "job"
        expected_jobs = [self.job_1, self.job_3]
        job_location = ITALY

        self._assert_search_by_distance(job_location, query, expected_jobs,
                                        precision=5)

    def _assert_search_by_distance(self, job_location, query, expected_jobs,
                                   precision):
        location = get_coordinates_from_location(self.current_location)
        location_str = ",".join([str(l) for l in location])

        radius_km = distance_from_location(location, job_location) + precision
        params = urlencode({
            'query': query,
            'location': location_str,
            'radius': radius_km
        })
        self._assert_search(expected_jobs, params)

    def _assert_search(self, expected_jobs, url_params):
        url = "{root}?{params}".format(root=SEARCH, params=url_params)
        response = self.get_data(url)
        self.assertEqual(200, response.status_code)
        results = json.loads(response.data)
        jobs = results['jobs']
        self.assertEquals([j['title'] for j in expected_jobs],
                          [j['title'] for j in jobs])

    @classmethod
    def _crate_job(cls, **job_args):
        job = cls.create_from_factory(JobFactory, **job_args)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=15)
        advert_id = advert['_id']

        request_approval_job_advert(job_id=job_id, advert_id=advert_id)
        approve_job_advert(job_id=job_id, advert_id=advert_id)
        publish_job_advert(job_id=job_id, advert_id=advert_id)

        return job

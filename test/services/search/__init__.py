from datetime import datetime, timedelta

from db.collections import _create_text_index, jobs
from model.job.job_advert import add_advert_to_job, \
    request_approval_job_advert, approve_job_advert, publish_job_advert
from services.search import search
from test import UnitTestCase
from test.model.job import JobFactory

EDINBURGH_CENTER = {
    "postcode": "EH3 9DZ", "admin_district": "Edinburgh",
    "latitude": 55.9544088, "longitude": -3.1700107
}

EDINBURGH_ZOO = {
    "postcode": "EH3 9DZ", "admin_district": "Edinburgh",
    "latitude": 55.9421766, "longitude": -3.2848378
}

EDINBURGH_ARTHURS_SEAT = {
    "postcode": "EH3 9DZ", "admin_district": "Edinburgh",
    "latitude": 55.9400444, "longitude": -3.192663
}

EDINBURGH_EICA = {
    "postcode": "EH3 9DZ", "admin_district": "Edinburgh",
    "latitude": 55.923412, "longitude": -3.3998947
}

EDINBURGH_ROSELIN_CHAPEL = {
    "postcode": "EH3 9DZ", "admin_district": "Edinburgh",
    "latitude": 55.8538158, "longitude": -3.1861218
}

STERLING_CASTLE = {
    "postcode": "FK8 1EJ", "admin_district": "Sterling",
    "latitude": 56.1238708, "longitude": -3.9470077
}

ITALY = {
    "postcode": "None", "admin_district": "None",
    "latitude": 45.8557706, "longitude": 13.056929
}


class BaseSearchTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        _create_text_index()

    @classmethod
    def _crate_job(cls,
                   duration=15, published=True, expired=False, **job_args):
        job = cls.create_from_factory(JobFactory, **job_args)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=duration)
        advert_id = advert['_id']

        request_approval_job_advert(job_id=job_id, advert_id=advert_id)
        approve_job_advert(job_id=job_id, advert_id=advert_id)
        if published:
            publish_job_advert(job_id=job_id, advert_id=advert_id)

        if expired:
            cls._make_advert_expired(job_id=job_id, advert_id=advert_id)

        return job

    @classmethod
    def _make_advert_expired(cls, job_id, advert_id):
        yesterday = datetime.now() - timedelta(days=1)
        jobs.update(
            {'_id': job_id, 'adverts._id': advert_id},
            {"$set": {'adverts.$.date.expires': yesterday}}
        )

    def _assert_search(self, expected_jobs, comparator='title',
                       **search_params):
        results, _, _ = search(**search_params)
        self.assertEquals([j[comparator] for j in expected_jobs],
                          [r[comparator] for r in results])

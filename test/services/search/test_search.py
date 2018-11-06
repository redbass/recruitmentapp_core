from datetime import datetime, timedelta

from db.collections import jobs, _create_text_index
from lib.geo import km2rad
from model.geo_location import get_location
from model.job.job_advert import add_advert_to_job, approve_job_advert, \
    publish_job_advert
from services.search import search
from test import UnitTestCase
from test.model.job import JobFactory
from test.services.search import EDINBURGH_ARTHURS_SEAT, EDINBURGH_ZOO, \
    EDINBURGH_EICA, EDINBURGH_ROSELIN_CHAPEL, EDINBURGH_CENTER, ITALY


class BaseSearchTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        _create_text_index()

        self.guide = self._crate_job(
            title="Tourist guide Job", description="Description ten",
            location=EDINBURGH_ROSELIN_CHAPEL)

        self.breeder = self._crate_job(
            title="Breeder job", description="Something Else",
            location=EDINBURGH_ZOO)

        self.climber = self._crate_job(
            title="Climber", description="Description eleven",
            location=EDINBURGH_EICA)

        self.far_job = self._crate_job(
            title="Far Far away", description="this job is in italy",
            location=ITALY)

        self.expiredJob = self._crate_job(
            title="Expired Job", description="This is an expired job",
            location=EDINBURGH_EICA,
            expired=True)

        self.job_not_publish = self.create_from_factory(
            JobFactory, title="Climber", description="Description eleven",
            location=EDINBURGH_ARTHURS_SEAT)

    @classmethod
    def _crate_job(cls, duration=15, expired=False, **job_args):
        job = cls.create_from_factory(JobFactory, **job_args)
        job_id = job['_id']
        advert = add_advert_to_job(job_id=job_id,
                                   advert_duration_days=duration)
        advert_id = advert['_id']

        approve_job_advert(job_id=job_id, advert_id=advert_id)
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


class SearchTextTestCase(BaseSearchTestCase):

    def test_search_jobs_by_title(self):
        results = list(search('Job'))

        self.assertEqual(3, len(results))
        expected_jobs = [self.guide, self.breeder, self.far_job
                         ]

        self.assertEquals([j['title'] for j in expected_jobs],
                          [r['title'] for r in results])

    def test_search_jobs_by_description(self):
        results = list(search('Description'))

        self.assertEqual(2, len(results))
        expected_jobs = [self.climber, self.guide]

        self.assertEquals([j['title'] for j in expected_jobs],
                          [r['title'] for r in results])

        self.assertEqual(2, len(results))
        self.assertEqual(self.climber['title'], results[0]['title'])
        self.assertEqual(self.guide['title'], results[1]['title'])

    def test_search_jobs_by_title_and_description(self):
        results = list(search('breeder eleven'))

        self.assertEqual(2, len(results))
        self.assertEqual(self.climber['title'], results[0]['title'])
        self.assertEqual(self.breeder['title'], results[1]['title'])

    def test_search_jobs_by_lowercase(self):
        results = list(search('climber'))

        self.assertEqual(1, len(results))
        self.assertEqual(self.climber['title'], results[0]['title'])

    def test_search_jobs_no_results(self):
        results = list(search('NOTHING'))

        self.assertEqual(0, len(results))


class SearchByLocationTestCase(BaseSearchTestCase):

    def setUp(self):
        super().setUp()
        self.city_center = get_location(
            **EDINBURGH_CENTER)['geo_location']['coordinates']

    def test_search_advert_by_radius_6km(self):
        rad = km2rad(6)
        results = search(query="Job", location=self.city_center,
                         radius=rad)
        results = list(results)

        self.assertEqual(1, len(results))

    def test_search_advert_by_radius_11km(self):
        rad = km2rad(11)
        results = search(query="Job eleven", location=self.city_center,
                         radius=rad)
        results = list(results)

        self.assertEqual(2, len(results))

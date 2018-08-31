from datetime import datetime, timedelta

from freezegun import freeze_time

from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, _create_advert_dict, \
    AdvertStatus, approve_job_advert, publish_job_advert
from test.model.job import BaseTestJob, JobFactory


class BaseTestJobAdvert(BaseTestJob):

    def setUp(self):
        super().setUp()
        self.job = self.create_from_factory(JobFactory)
        self.job_id = self.job['_id']


class TestAddJobAdvert(BaseTestJobAdvert):

    def test_add_job_advert(self):
        days = 15

        add_advert_to_job(job_id=self.job_id, advert_duration_days=days)

        stored_job = get_job(job_id=self.job_id)
        stored_adverts = stored_job['adverts']

        self.assertEquals(1, len(stored_adverts))
        stored_advert = stored_adverts[0]

        self.assertEquals(AdvertStatus.DRAFT, stored_advert['status'])
        self.assertEquals(days, stored_advert['duration'])

    def test_add_advert_to_invalid_job(self):
        job_id = "RANDOM"
        with self.assertRaisesRegex(
                ValueError,
                'The job with id `{job_id}` has not been found'
                .format(job_id=job_id)):
            add_advert_to_job(job_id=job_id, advert_duration_days=15)


class TestSetStatusJobAdvert(BaseTestJobAdvert):

    def setUp(self):
        super().setUp()
        self.days = 15
        self.advert = add_advert_to_job(
            job_id=self.job_id, advert_duration_days=self.days)
        self.advert_id = self.advert['_id']

    def test_approve_job(self):
        approve_job_advert(advert_id=self.advert_id, job_id=self.job_id)

        stored_job = get_job(job_id=self.job_id)
        stored_advert = stored_job['adverts'][0]

        self.assertEquals(AdvertStatus.APPROVED, stored_advert['status'])
        self.assertEquals(self.days, stored_advert['duration'])

    @freeze_time("2015-10-26")
    def test_publish_job(self):
        approve_job_advert(advert_id=self.advert_id, job_id=self.job_id)
        publish_job_advert(advert_id=self.advert_id, job_id=self.job_id)
        expires_at = datetime.now() + timedelta(days=self.days)

        stored_job = get_job(job_id=self.job_id)
        stored_advert = stored_job['adverts'][0]

        self.assertEquals(AdvertStatus.PUBLISHED, stored_advert['status'])
        self.assertEquals(self.days, stored_advert['duration'])
        self.assertEquals(expires_at, stored_advert['date']['expires'])

    def test_approve_non_draft_advert(self):
        approve_job_advert(advert_id=self.advert_id, job_id=self.job_id)
        publish_job_advert(advert_id=self.advert_id, job_id=self.job_id)

        with self.assertRaisesRegex(ValueError,
                                    'Impossible to update the advert status'):
            approve_job_advert(advert_id=self.advert_id, job_id=self.job_id)

    def test_publish_non_approved_advert(self):
        approve_job_advert(advert_id=self.advert_id, job_id=self.job_id)
        publish_job_advert(advert_id=self.advert_id, job_id=self.job_id)

        with self.assertRaisesRegex(ValueError,
                                    'Impossible to update the advert status'):
            publish_job_advert(advert_id=self.advert_id, job_id=self.job_id)


class TestJobAdvertMethods(BaseTestJob):
    freeze_date = datetime(year=1985, month=10, day=26)

    def test_advert_status_equality(self):
        self.assertEqual(AdvertStatus.DRAFT, AdvertStatus.DRAFT)
        self.assertEqual(AdvertStatus.DRAFT, "DRAFT")

        self.assertNotEqual(AdvertStatus.DRAFT, AdvertStatus.APPROVED)
        self.assertNotEqual(AdvertStatus.DRAFT, "something")

    @freeze_time(freeze_date)
    def test_create_advert_dict(self):
        duration = 30
        advert = _create_advert_dict(duration=duration)
        expected_advert = {
            '_id': advert['_id'],
            'status': AdvertStatus.DRAFT,
            'duration': duration,
            'date': {
                'created': datetime.utcnow(),
                'updated': datetime.utcnow()
            }
        }
        self.assertEqual(expected_advert, advert)

    def test_create_advert_with_wrong_period(self):
        self._assert_invalid_duration(0)
        self._assert_invalid_duration(-1)

    def _assert_invalid_duration(self, duration):
        with self.assertRaisesRegex(
                ValueError,
                "'{d}' is not a valid duration".format(d=duration)):
            _create_advert_dict(duration=duration)

from datetime import datetime
from unittest.mock import patch, ANY

from freezegun import freeze_time

from model.job.job import get_job
from model.job.job_advert import add_advert_to_job, _create_advert_dict, \
    approve_job_advert, publish_job_advert, pay_job_advert, \
    publish_payed_job_advert, request_approval_job_advert, \
    _update_advert_status, archive_job_advert
from model.job import AdvertStatus

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
        add_advert_to_job(job_id=self.job_id, advert_duration_days=self.days)
        self.advert = add_advert_to_job(
            job_id=self.job_id, advert_duration_days=self.days)
        add_advert_to_job(job_id=self.job_id, advert_duration_days=self.days)
        self.advert_id = self.advert['_id']

    def test_request_approval_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=request_approval_job_advert,
            allowed_statuses=[AdvertStatus.DRAFT],
            new_status=AdvertStatus.REQUEST_APPROVAL)

    def test_approve_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=approve_job_advert,
            allowed_statuses=[AdvertStatus.DRAFT,
                              AdvertStatus.REQUEST_APPROVAL],
            new_status=AdvertStatus.APPROVED)

    def test_pay_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=pay_job_advert,
            allowed_statuses=[AdvertStatus.APPROVED],
            new_status=AdvertStatus.PAYED)

    def test_publish_payed_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=publish_payed_job_advert,
            allowed_statuses=[AdvertStatus.PAYED],
            new_status=AdvertStatus.PUBLISHED)

    def test_publish_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=publish_job_advert,
            allowed_statuses=[AdvertStatus.APPROVED,
                              AdvertStatus.PAYED],
            new_status=AdvertStatus.PUBLISHED)

    def test_archive_job_advert(self):
        self._assert_called_update_advert_status_with(
            func=archive_job_advert,
            allowed_statuses=[AdvertStatus.PUBLISHED],
            new_status=AdvertStatus.ARCHIVED)

    def test_update_advert_status_base_case(self):
        new_status = "random_value"
        _update_advert_status(advert_id=self.advert_id,
                              job_id=self.job_id,
                              allowed_statuses=[AdvertStatus.DRAFT],
                              new_status=new_status)
        self._assert_job_status(expected_status=new_status)

    def test_update_advert_status_new_status_PUBLISHED_set_expire_date(self):
        new_status = AdvertStatus.PUBLISHED
        _update_advert_status(advert_id=self.advert_id,
                              job_id=self.job_id,
                              allowed_statuses=[AdvertStatus.DRAFT],
                              new_status=new_status)
        self._assert_job_status(expected_status=new_status,
                                expected_expires_date=ANY)

    def _assert_job_status(self, expected_status, expected_expires_date=None):
        default_status = AdvertStatus.DRAFT
        stored_job = get_job(job_id=self.job_id)
        first_advert = stored_job['adverts'][0]
        last_advert = stored_job['adverts'][-1]
        modified_advert = stored_job['adverts'][1]
        self.assertEquals(default_status, first_advert['status'])
        self.assertEquals(expected_status, modified_advert['status'])
        self.assertEquals(default_status, last_advert['status'])
        self.assertEquals(self.days, modified_advert['duration'])
        self.assertEquals(expected_expires_date,
                          modified_advert['date'].get('expires'))

    def _assert_called_update_advert_status_with(self, func,
                                                 allowed_statuses, new_status):
        with patch('model.job.job_advert._update_advert_status') as mock:
            func(job_id=self.job_id, advert_id=self.advert_id)
            mock.assert_called_once_with(
                advert_id=self.advert_id,
                job_id=self.job_id,
                allowed_statuses=allowed_statuses,
                new_status=new_status)


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

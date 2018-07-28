from datetime import datetime

from freezegun import freeze_time

from model.advert import AdvertStatus
from model.job.job import get_job
from model.job.create_job import create_job
from model.job.job_advert import create_advert_for_a_job, update_advert_status
from test.model.job import BaseTestJob


class TestSetAdvertStatus(BaseTestJob):

    def setUp(self):
        super().setUp()
        self.advert_created_at = datetime(year=2345, month=12, day=21)
        self.advert_duration = 30

        with freeze_time(self.advert_created_at):
            self.job = create_job(company_id=self.company['_id'],
                                  title='Title', description='Description')
            self.advert = create_advert_for_a_job(
                job_id=self.job['_id'], advert_duration=self.advert_duration)

    def _assert_set_status(self, new_status):
        advert_updated_at = datetime(year=1234, month=12, day=12)

        with freeze_time(advert_updated_at):
            update_advert_status(job_id=self.job['_id'],
                                 advert_id=self.advert['_id'],
                                 new_status=new_status)

        retrieved_job = get_job(self.job['_id'])
        retrieved_advert = retrieved_job['adverts'][0]
        expected_advert = {
            '_id': self.advert['_id'],
            'status': new_status,
            'duration': self.advert_duration,
            'date': {
                new_status.lower(): advert_updated_at,
                'created': self.advert_created_at,
                'updated': advert_updated_at
            },
            'status_log': [{
                'status': new_status,
                'date': advert_updated_at
            }]
        }
        self.assertEqual(advert_updated_at, retrieved_job['date']['updated'])
        self.assertEqual(expected_advert, retrieved_advert)

    def test_publish_advert(self):
        self._assert_set_status(new_status=AdvertStatus.PUBLISHED)

    def test_approve_advert(self):
        self._assert_set_status(new_status=AdvertStatus.APPROVED)

    def test_set_status_with_wrong_id(self):
        self._assert_approve_advert_wrong_ids(job_id="123",
                                              advert_id="RANDOM")
        self._assert_approve_advert_wrong_ids(job_id=self.job['_id'],
                                              advert_id="RANDOM")

    def _assert_approve_advert_wrong_ids(self, job_id, advert_id):
        with self.assertRaisesRegex(
                ValueError, 'The advert is not in `DRAFT` or does not exists:'
                            '\(job: `.*, advert: `.*`\)'):
            update_advert_status(job_id=job_id, advert_id=advert_id,
                                 new_status=AdvertStatus.APPROVED)

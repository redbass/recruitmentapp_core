from freezegun import freeze_time

from model.job import create_job, get_job
from test.model.job import BaseTestJob


class TestGetJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_get_job(self):
        expected_job = create_job(title="title", description="description")
        job_id = expected_job['_id']

        job = get_job(job_id)

        self.assertEqual(expected_job, job)

    def test_get_job_invalid_id(self):
        create_job(title="title", description="description")

        job = get_job(None)
        self.assertEqual(None, job)

        job = get_job("")
        self.assertEqual(None, job)

from db.collections import jobs
from model.job import create_job, delete_jobs, get_jobs
from test_integration import IntegrationTestCase


class TestCreateJob(IntegrationTestCase):

    def tearDown(self):
        jobs.drop()

    def test_create_job(self):
        title = 'The title'
        description = 'Job Description!'

        expected_job1 = create_job(title + '1', description + '1')
        expected_job2 = create_job(title + '2', description + '2')

        created_job1 = get_jobs([expected_job1['_id']])
        created_job2 = get_jobs([expected_job2['_id']])

        self.assertEqual(created_job1[0], expected_job1)
        self.assertEqual(created_job2[0], expected_job2)

    def test_delete_job(self):
        job = create_job('title', 'description')

        delete_jobs([job['_id']])

        deleted_jobs = get_jobs([job['_id']])
        self.assertTrue(deleted_jobs[0].get('deleted'))

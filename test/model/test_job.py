from unittest import TestCase
from unittest.mock import patch

from model.job import create_job, delete_jobs, get_jobs


class TestCreateJob(TestCase):

    @patch('model.job.create_id')
    @patch('model.job.jobs')
    def test_create_job(self, jobs, create_id):

        expected_id = '123'
        expected_title = 'title'
        expected_description = 'description'
        expected_job = {
            '_id': expected_id,
            'title': expected_title,
            'description': expected_description,
            'period': {
                'start': None,
                'stop': None
            },
            'draft': False,
            'deleted': False
        }

        create_id.return_value = expected_id

        created_job = create_job(
            title=expected_job['title'],
            description=expected_job['description']
        )

        self.assertEqual(created_job, expected_job)
        self.assertTrue(jobs.insert_one.called)

    def test_create_job_parameters_error(self):
        self.assertRaises(AttributeError, create_job, None, None)
        self.assertRaises(AttributeError, create_job, '', '')
        self.assertRaises(AttributeError, create_job, '123', None)
        self.assertRaises(AttributeError, create_job, None, 'asd')


class TestDeleteJobs(TestCase):

    @patch('model.job.jobs')
    def test_delete_jobs(self, jobs):
        job_to_delete_ids = ["123"]
        delete_jobs(job_to_delete_ids)

        call_args = jobs.update_many.call_args[0]
        self.assertEqual(call_args[0], {'_id': {'$in': job_to_delete_ids}})
        self.assertEqual(call_args[1], {'$set': {'deleted': True}})

    def test_delete_jobs_parameter_error(self):
        self.assertRaises(AttributeError, delete_jobs, None)
        self.assertRaises(AttributeError, delete_jobs, [])
        self.assertRaises(AttributeError, delete_jobs, '123')


class TestGetJobs(TestCase):

    @patch('model.job.jobs')
    def test_get_jobs(self, jobs):
        _ids = ["123"]
        expected_job = {}
        jobs.find.return_value = [expected_job]

        result = get_jobs(_ids)

        self.assertEqual(result[0], expected_job)

    def test_get_jobs_parameter_error(self):
        self.assertRaises(AttributeError, delete_jobs, None)
        self.assertRaises(AttributeError, delete_jobs, [])
        self.assertRaises(AttributeError, delete_jobs, '123')

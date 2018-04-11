from unittest.mock import patch

from model.job import create_job, delete_jobs, get_jobs, get_all_jobs, \
    DEFAULT_JOBS_PAGINATION_LIMIT, DEFAULT_JOBS_PAGINATION_START
from test import UnitTestCase


class TestCreateJob(UnitTestCase):

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


class TestDeleteJobs(UnitTestCase):

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


class TestGetJobs(UnitTestCase):

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


class TestGetAllJobs(UnitTestCase):

    @patch('model.job.jobs')
    @patch('model.job.get_pagination_from_cursor')
    def test_get_all_jobs(self, get_pagination, jobs):
        expected_jobs = "expected_jobs"
        expected_cursor = "cursor"

        expected_pagination_start = 2
        expected_pagination_limit = 20

        jobs.find.return_value = expected_cursor
        get_pagination.return_value = expected_jobs

        results = get_all_jobs(start=expected_pagination_start,
                               limit=expected_pagination_limit)

        self.assertEqual(results, expected_jobs)
        jobs.find.assert_called_once_with({})
        get_pagination.assert_called_once_with(expected_cursor,
                                               expected_pagination_start,
                                               expected_pagination_limit)

    @patch('model.job.jobs')
    @patch('model.job.get_pagination_from_cursor')
    def test_get_all_jobs_null_params(self, get_pagination, jobs):
        expected_jobs = "expected_jobs"
        expected_cursor = "cursor"

        jobs.find.return_value = expected_cursor
        get_pagination.return_value = expected_jobs

        results = get_all_jobs(limit=None, start=None)

        self.assertEqual(results, expected_jobs)
        jobs.find.assert_called_once_with({})
        get_pagination.assert_called_once_with(expected_cursor,
                                               DEFAULT_JOBS_PAGINATION_START,
                                               DEFAULT_JOBS_PAGINATION_LIMIT)

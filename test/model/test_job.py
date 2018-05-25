from datetime import datetime

from freezegun import freeze_time

from db.collections import jobs
from model.job import create_job, delete_jobs, add_avert_to_job, get_job
from model.location import Location
from test import UnitTestCase


class BaseTestJob(UnitTestCase):

    def tearDown(self):
        super().tearDown()
        jobs.drop()


class TestCreateJob(UnitTestCase):

    @freeze_time("2015-10-26")
    def test_create_job(self):
        expected_job = {
            'title': 'title',
            'description': 'description',
            'period': {
                'start': datetime.now(),
                'end': None
            },
            'location': None,
            'deleted': False
        }

        created_job = create_job(
            title=expected_job['title'],
            description=expected_job['description']
        )
        created_job_id = created_job.get('_id')

        expected_job['_id'] = created_job_id
        self.assertEqual(created_job, expected_job)

        stored_job = get_job(created_job_id)
        self.assertEqual(stored_job, expected_job)

    def test_create_job_parameters_error(self):
        self.assertRaises(AttributeError, create_job, None, None)
        self.assertRaises(AttributeError, create_job, '', '')
        self.assertRaises(AttributeError, create_job, '123', None)
        self.assertRaises(AttributeError, create_job, None, 'asd')

    def test_create_job_with_location(self):
        location = Location(10, 20)
        created_job = create_job(location=location,
                                 title='test',
                                 description='test description')

        self.assertEqual(created_job['location'],
                         location.get_geo_json_point())

        stored_job = get_job(created_job['_id'])
        self.assertEqual(stored_job['location'], location.get_geo_json_point())


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


class TestDeleteJobs(UnitTestCase):

    def test_delete_jobs(self):
        job = create_job(title="title", description="description")
        job_id = job['_id']
        delete_jobs([job_id])

        stored_job = get_job(job_id)

        self.assertTrue(stored_job['deleted'])

    def test_delete_jobs_parameter_error(self):
        self.assertRaises(AttributeError, delete_jobs, None)
        self.assertRaises(AttributeError, delete_jobs, [])
        self.assertRaises(AttributeError, delete_jobs, '123')


class TestAddAdvertToJob(BaseTestJob):

    def test_add_avert_to_job(self):
        title = "Some title"
        description = "Some description"
        job = create_job(title=title, description=description)
        advert1 = {
            "advert": 1}
        advert2 = {
            "advert": 2}
        job_id = job['_id']

        add_avert_to_job(job_id=job_id, advert=advert1)
        add_avert_to_job(job_id=job_id, advert=advert2)

        result = jobs.find_one({
                                   '_id': job_id})

        expected_adverts = [advert1, advert2]
        self.assertEqual(result['adverts'], expected_adverts)

    def test_add_avert_to_job_with_invalid_id(self):
        add_avert_to_job(job_id=None, advert={
            "advert": 1})
        add_avert_to_job(job_id="", advert={
            "advert": 2})

        result = jobs.find({}).count()

        self.assertEqual(0, result)

    def test_add_avert_to_job_with_invalid_advert(self):
        with self.assertRaises(ValueError):
            add_avert_to_job(job_id="123", advert={})

        with self.assertRaises(ValueError):
            add_avert_to_job(job_id="123", advert=None)

        with self.assertRaises(ValueError):
            add_avert_to_job(job_id="123", advert="")

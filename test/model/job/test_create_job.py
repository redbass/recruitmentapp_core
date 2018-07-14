from datetime import datetime

from freezegun import freeze_time

from model.job.job import get_job
from model.job.create_job import create_job
from model.location import Location
from test.model.job import BaseTestJob


class TestCreateJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_create_job(self):
        expected_job = {
            'company_id': self.company['_id'],
            'title': 'title',
            'description': 'description',
            'location': None,
            'deleted': False,
            'date': {
                'created': datetime.utcnow(),
                'updated': datetime.utcnow()
            }
        }

        created_job = create_job(
            company_id=expected_job['company_id'],
            title=expected_job['title'],
            description=expected_job['description']
        )
        created_job_id = created_job.get('_id')

        expected_job['_id'] = created_job_id
        self.assertEqual(created_job, expected_job)

        stored_job = get_job(created_job_id)
        self.assertEqual(stored_job, expected_job)

    def test_create_job_parameters_error(self):
        self.assertRaises(AttributeError, create_job, None, '123', 'asd')
        self.assertRaises(AttributeError, create_job, '', '123', 'asd')
        self.assertRaises(AttributeError, create_job, 'abc', None, 'asd')
        self.assertRaises(AttributeError, create_job, 'abc', '', 'asd')
        self.assertRaises(AttributeError, create_job, 'abc', '123', None)
        self.assertRaises(AttributeError, create_job, 'abc', '123', '')

    def test_create_job_with_invalid_company_id(self):
        self.assertRaises(ValueError,
                          create_job, 'invalid_company', '123', 'asd')

    def test_create_job_with_location(self):
        location = Location(10, 20)
        created_job = create_job(company_id=self.company['_id'],
                                 location=location,
                                 title='test',
                                 description='test description')

        self.assertEqual(created_job['location'],
                         location.get_geo_json_point())

        stored_job = get_job(created_job['_id'])
        self.assertEqual(stored_job['location'], location.get_geo_json_point())

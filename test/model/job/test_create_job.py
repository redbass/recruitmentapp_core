from freezegun import freeze_time

from model.job.create_job import create_job
from model.job.job import get_job
from test.model.company import CompanyFactory
from test.model.job import BaseTestJob


class TestCreateJob(BaseTestJob):

    @freeze_time("2015-10-26")
    def test_create_job(self):
        input_job = self._get_test_create_job_input()
        created_job = create_job(**input_job)

        stored_job = get_job(created_job['_id'])
        self.assert_validate_json_schema('job', stored_job)

    def test_validate_company_id(self):
        input_job = self._get_test_create_job_input()
        input_job['company_id'] = "SOMETHING"

        with self.assertRaisesRegex(
                ValueError, 'The company_id `{company_id}` is invalid'.format(
                    company_id=input_job['company_id'])):
            create_job(**input_job)

    def test_validate_location(self):
        input_job = self._get_test_create_job_input()
        input_job['location']['latitude'] = 10000

        with self.assertRaisesRegex(
                ValueError,
                'Latitude value have to be -90 <= latitude <= 90'):
            create_job(**input_job)

    def _get_test_create_job_input(self):
        company = self.create_from_factory(CompanyFactory)
        job = {
            "company_id": company['_id'],
            "title": "Some title",
            "description": "Some long description",
            "duration_days": 28,
            "location": {
                "postcode": "eh8 8hf",
                "admin_district": "Edinburgh",
                "latitude": -3.168018,
                "longitude": 55.95511
            },
            "metadata": {
                "trades": ["software_engineer"],
                "job_type": "developer"
            },
            "rate": {
                "type": "other",
                "units": "lines of code",
                "value": 0.1
            }
        }
        return job

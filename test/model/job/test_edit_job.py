from model.job.edit_job import edit_job
from model.job.create_job import create_job
from model.job.job import get_job
from model.location import Location
from test.model.job import BaseTestJob


class TestEditJob(BaseTestJob):

    def setUp(self):
        super().setUp()
        self.location = Location(10, 20)
        self.job = create_job(company_id=self.company['_id'],
                              title="Old Job Title",
                              description="Old Description",
                              location=self.location)

    def test_update_job(self):

        job_id = self.job['_id']
        new_title = "New title"
        new_description = "New Description"
        new_location = Location(0, 0)

        edit_job(job_id=job_id, new_title=new_title,
                 new_description=new_description, new_location=new_location)

        updated_job = get_job(job_id)

        self.assertEqual(new_title, updated_job['title'])
        self.assertEqual(new_description, updated_job['description'])
        self.assertEqual(new_location.get_geo_json_point(),
                         updated_job['location'])

    def test_invalid_id_raises_exception(self):

        with self.assertRaisesRegex(ValueError,
                                    "Job id '.*' invalid or not found"):
            edit_job(job_id="INVALID", new_title="something")

    def test_partial_update(self):

        job_id = self.job['_id']
        new_title = "New title"

        original_job = get_job(job_id)

        edit_job(job_id=job_id, new_title=new_title)

        updated_job = get_job(job_id)

        self.assertEqual(new_title, updated_job['title'])
        self.assertEqual(original_job['description'],
                         updated_job['description'])
        self.assertEqual(original_job['location'],
                         updated_job['location'])

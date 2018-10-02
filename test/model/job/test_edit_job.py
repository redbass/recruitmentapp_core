from model.job.edit_job import edit_job
from model.job.job import get_job
from test.model.job import BaseTestJob, JobFactory


class TestEditJob(BaseTestJob):

    def setUp(self):
        super().setUp()
        self.job = self.create_from_factory(JobFactory)

    def test_update_job(self):

        job_id = self.job['_id']
        new_title = "New title"
        new_description = "New Description"

        edit_job(_id=job_id, title=new_title, description=new_description)

        updated_job = get_job(job_id)

        self.assertEqual(new_title, updated_job['title'])
        self.assertEqual(new_description, updated_job['description'])

    def test_invalid_id_raises_exception(self):

        with self.assertRaisesRegex(ValueError,
                                    "Job id '.*' invalid or not found"):
            edit_job(_id="INVALID", title="something")

    def test_cannot_modify_company_id(self):

        with self.assertRaisesRegex(ValueError,
                                    "Job's company cannot be modified"):
            edit_job(_id="INVALID", company_id="something")

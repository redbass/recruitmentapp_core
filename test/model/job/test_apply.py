from model.job.application import apply_advert, get_advert_applications, \
    get_advert_applications_by_job_id
from model.job.job_advert import add_advert_to_job
from test.model.job import BaseTestJob, JobFactory


class TestApplication(BaseTestJob):

    def setUp(self):
        super().setUp()
        self.candidate = {
            'candidate_id': '1',
            'email': 'email@io.it',
            'first_name': 'Name',
            'last_name': 'Last',
            'phone_number': '123123123',
            'metadata': {
                "some": "data"
            }
        }

    def test_create_application(self):
        advert_id = 123
        apply_advert(advert_id=advert_id, **self.candidate)

        applications = get_advert_applications(advert_id=advert_id)
        self.assertEqual(1, len(applications['candidates']))

        first_candidate = applications['candidates'][0]
        self.assertEqual(self.candidate, first_candidate)

    def test_get_advert_applications_by_job_id(self):
        job = self.create_from_factory(JobFactory)
        advert_1 = add_advert_to_job(job_id=job['_id'],
                                     advert_duration_days=19)
        advert_2 = add_advert_to_job(job_id=job['_id'],
                                     advert_duration_days=19)
        apply_advert(advert_id=advert_1['_id'], **self.candidate)
        apply_advert(advert_id=advert_2['_id'], **self.candidate)

        applications = get_advert_applications_by_job_id(job_id=job['_id'])

        self.assertEqual([self.candidate, self.candidate],
                         applications['candidates'])

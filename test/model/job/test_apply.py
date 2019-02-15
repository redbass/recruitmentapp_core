from model.job.application import apply_advert, get_advert_applications
from test.model.job import BaseTestJob


class TestApplication(BaseTestJob):

    def test_create_application(self):
        advert_id = "123"
        candidate = {
            'candidate_id': '1',
            'email': 'email@io.it',
            'first_name': 'Name',
            'last_name': 'Last',
            'phone_number': '123123123',
            'metadata': {
                "some": "data"
            }
        }
        apply_advert(advert_id=advert_id, **candidate)

        applications = get_advert_applications(advert_id=advert_id)
        self.assertEqual(1, len(applications['candidates']))

        first_candidate = applications['candidates'][0]
        self.assertEqual(candidate, first_candidate)

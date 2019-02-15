from api.routes.routes import APPLY_ADVERT
from model.job.application import get_advert_applications
from test.api import TestApi


class TestAdvert(TestApi):

    def test_apply_advert(self):

        advert_id = "123"
        candidate = {
            "candidate_id": "candidate_id",
            "email": "email",
            "first_name": "name",
            "last_name": "surname",
            "phone_number": "070707089",
            "metadata": {
                "years_experience": 1,
                "cards": "something"
            }
        }

        url = self.url_for(APPLY_ADVERT, advert_id=advert_id)
        response = self.post_json(url, candidate)

        self.assertEqual(200, response.status_code)

        application = get_advert_applications(advert_id=advert_id)

        self.assertEqual(candidate, application['candidates'][0])

from db.collections import jobs, companies, users
from lib.geo import km2rad
from model.company.company import create_company
from model.job.create_job import create_job
from model.user import create_user, UserType
from search.job import search_adverts_by_radius
from test import UnitTestCase

from test.search import EDINBURGH_CENTER, EDINBURGH_ZOO, \
    EDINBURGH_ROSELIN_CHAPEL


class SearchAdvertByRadiusTestCase(UnitTestCase):

    def setUp(self):
        super().setUp()
        self.admin = create_user(username='admin', password="password",
                                 email="email@posta.it",
                                 user_type=UserType.ADMIN)
        self.zoo = create_company(name="Edinburgh Zoo",
                                  description="desc",
                                  admin_user_id=self.admin['_id'])
        self.chapel = create_company(name="Edinburgh Roselin chapel",
                                     description="desc",
                                     admin_user_id=self.admin['_id'])
        self._create_jobs()

    def tearDown(self):
        super().tearDown()
        jobs.drop()
        users.drop()
        companies.drop()

    def test_search_advert_by_radius_5km(self):
        rad = km2rad(6)
        results = search_adverts_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 1)

    def test_search_advert_by_radius_11km(self):
        rad = km2rad(11)
        results = search_adverts_by_radius(EDINBURGH_CENTER, rad)

        self.assertEqual(results.count(), 2)

    def _create_jobs(self):
        self.edinburgh_center = create_job(
            company_id=self.zoo['_id'],
            title="Breeder",
            description="Breeder Description",
            location=EDINBURGH_ZOO)
        self.edinburgh_center = create_job(
            company_id=self.chapel['_id'],
            title="Templar",
            description="Templar Description",
            location=EDINBURGH_ROSELIN_CHAPEL)

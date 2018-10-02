from model.job.create_job import create_job
from test import UnitTestCase
from test import load_example_model
from test.factory import ModelFactory
from test.model.company import CompanyFactory


class BaseTestJob(UnitTestCase):
    pass


class JobFactory(ModelFactory):

    EXAMPLE_MODEL_NAME = 'create_job_input'

    def create(self, **qwargs):

        default_values = load_example_model(self.EXAMPLE_MODEL_NAME)

        if 'company_id' not in qwargs:
            company = self.create_from_factory(CompanyFactory)
            default_values['company_id'] = company['_id']

        default_values.update(qwargs)

        return create_job(**default_values)

from model.user import create_user
from test import load_example_model
from test.factory import ModelFactory


class UserFactory(ModelFactory):
    EXAMPLE_MODEL_NAME = 'create_user_input'

    def create(self, **qwargs):

        default_values = load_example_model(self.EXAMPLE_MODEL_NAME)

        if 'username' not in qwargs:
            default_values['username'] = self.fake.user_name()

        if 'email' not in qwargs:
            default_values['email'] = self.fake.email()

        default_values.update(qwargs)

        return create_user(**default_values)

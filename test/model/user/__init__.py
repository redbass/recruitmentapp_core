from model.user import create_user
from test import load_example_model
from test.factory import ModelFactory


class UserFactory(ModelFactory):
    MODEL_NAME = 'user'

    def create(self, **qwargs):

        default_values = load_example_model('create_user_input')

        default_values.update(qwargs)

        return create_user(**default_values)

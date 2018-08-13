from abc import ABC, abstractmethod

from faker import Faker


class ModelFactory(ABC):
    EXAMPLE_MODEL_NAME = None

    fake = Faker('en_GB')

    @abstractmethod
    def create(self, **qwargs):
        pass

    @classmethod
    def create_from_factory(cls, factory, **qwargs):
        return factory().create(**qwargs)

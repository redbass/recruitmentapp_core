from abc import ABC, abstractmethod


class ModelFactory(ABC):
    MODEL_NAME = None

    @abstractmethod
    def create(self, **qwargs):
        pass

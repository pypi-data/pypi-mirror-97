from abc import abstractmethod
import abc

from strategery.exceptions import TaskError


class StrategeryFeature(metaclass=abc.ABCMeta):
    @classmethod
    def strategery_key(cls):
        return cls

    @staticmethod
    @abstractmethod
    def compute(*args, **kwargs):
        raise NotImplementedError('StrategeryFeature must implement @staticmethod `compute`!')

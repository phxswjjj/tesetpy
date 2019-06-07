from abc import ABCMeta, abstractmethod
from .. import cadria


class TaskBase(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, w: cadria.wnd):
        pass
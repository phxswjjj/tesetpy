from abc import ABCMeta, abstractmethod

from ..scene import FeatureRule, SceneBase


class TaskWnd(metaclass=ABCMeta):
    @abstractmethod
    def is_scene(self, cls: SceneBase) -> bool:
        return NotImplemented

    @abstractmethod
    def match_rules(self, rules: [FeatureRule]) -> bool:
        return NotImplemented

    @property
    @abstractmethod
    def cur_scene(self) -> SceneBase:
        return NotImplemented


class TaskBase(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, w: TaskWnd):
        return NotImplemented

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

    @abstractmethod
    def mouse_move(self, from_rloc: tuple, to_rloc: tuple, rate: int = 1000):
        return NotImplemented

    @abstractmethod
    def mouse_left_click(self, rloc: tuple, times: int = 1):
        return NotImplemented


class TaskBase(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, w: TaskWnd):
        return NotImplemented

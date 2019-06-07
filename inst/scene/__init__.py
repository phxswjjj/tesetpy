from abc import ABCMeta, abstractmethod

from ..win32 import wcolor, wpos


class FeatureRule:
    def __init__(self, *args, **kwargs):
        self.pos: wpos = None
        self.color: wcolor = None


class WindowBase(metaclass=ABCMeta):
    pass


class SceneBase(metaclass=ABCMeta):
    def __init__(self):
        pass

    def match(self, w: WindowBase):
        if len(self.feature_rules) == 0:
            return False

        for rule in self.feature_rules:
            rule: FeatureRule
            return NotImplemented

    @abstractmethod
    def feature_rules(self):
        return NotImplemented

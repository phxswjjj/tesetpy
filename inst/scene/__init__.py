from abc import ABCMeta, abstractmethod

from ..win32 import wcolor, wpos


class FeatureRule:
    """
    場景特徵
    pos: wpos
    color: wcolor
    """

    def __init__(self, *args):
        """
        :param args:
        x, y, 'color'
        """
        self.pos: wpos = wpos(*args[:2])
        self.color: wcolor = wcolor(*args[2:])


class SceneBase(metaclass=ABCMeta):
    @abstractmethod
    def feature_rules(self) -> [FeatureRule]:
        return NotImplemented

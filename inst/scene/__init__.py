from abc import ABCMeta, abstractmethod
from collections import Iterable
from os import path as opath

import cv2
import numpy as np

from ..win32 import wcolor, wpos

_dir = 'inst/scene/img'


class FeatureRule:
    """
    場景特徵
    """
    # shared resources
    _res = dict()

    def __init__(self, filename: str):
        self._file_name = filename
        if filename not in FeatureRule._res:
            file_path = opath.join(_dir, filename)
            file_path = opath.abspath(file_path)
            img = cv2.imread(file_path)
            FeatureRule._res[filename] = img

    def match(self, img) -> bool:
        """符合特徵

        Arguments:
            img {array or image} -- 來源圖(screen)

        Returns:
            bool
        """
        screen_image: Iterable
        if isinstance(img, Iterable):
            screen_image = img
        else:
            screen_image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        find_image = self.image

        result = cv2.matchTemplate(
            screen_image, find_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc1, loc2 = np.where(result >= threshold)
        if len(loc1) > 0:
            return True
        else:
            return False

    @property
    def file_name(self):
        return self._file_name

    @property
    def image(self):
        return FeatureRule._res[self._file_name]


class SceneBase(metaclass=ABCMeta):
    @abstractmethod
    def feature_rules(self) -> [FeatureRule]:
        return NotImplemented

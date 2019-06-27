import cv2

from inst.cadria import wnd
from inst.scene import FeatureRule

from . import match

disconnect_img = cv2.imread('inst/scene/img/test_reconnect.jpg')


def test_wnd():
    w = wnd()
    w.load()
    assert w.hwnd != 0


def test_reconnect():
    rule_reconnect = FeatureRule('reconnect.jpg', 0.9)
    assert match([rule_reconnect], disconnect_img)

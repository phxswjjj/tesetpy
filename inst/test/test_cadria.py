import cv2

from inst.cadria import wnd
from inst.scene import FeatureRule

disconnect_img = cv2.imread('inst/scene/img/test_reconnect.jpg')
select_server_img = cv2.imread('inst/scene/img/test_select_server.jpg')

def test_wnd():
    w = wnd()
    w.load()
    assert w.hwnd != 0


def test_reconnect():
    rule_reconnect = FeatureRule('reconnect.jpg', 0.9)
    assert rule_reconnect.match(disconnect_img)
    assert not rule_reconnect.match(select_server_img)

def test_select_server():
    rule_enter = FeatureRule('select_server_enter.jpg', 0.9)
    assert rule_enter.match(select_server_img)
    assert not rule_enter.match(disconnect_img)

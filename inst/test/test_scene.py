import cv2

from inst.scene import FeatureRule, SceneBase
from inst.scene.forces import (ForcesWarExec, ForcesWarExecStep1,
                               ForcesWarExecStep2, ForcesWarQueue)
from inst.scene.pub import Pub
from inst.scene.shop import Shop

from . import match

shop_img = cv2.imread('inst/scene/img/test_shop.jpg')
pub_img = cv2.imread('inst/scene/img/test_pub.jpg')
forceswar_queue_img = cv2.imread('inst/scene/img/test_forceswar_queue.jpg')
forceswar_exec_img = cv2.imread('inst/scene/img/test_forceswar_exec.jpg')
forceswar_exec2_img = cv2.imread('inst/scene/img/test_forceswar_exec2.jpg')


def _match(s: SceneBase, screen_img) -> bool:
    rules: [FeatureRule] = s.feature_rules()
    return match(rules, screen_img)


def test_scenebase():
    subclasses: [SceneBase] = SceneBase.all_subclasses()
    assert Pub in subclasses
    assert Shop in subclasses
    assert ForcesWarQueue in subclasses
    assert ForcesWarExec not in subclasses
    assert ForcesWarExecStep1 in subclasses
    assert ForcesWarExecStep2 in subclasses


def test_shop():
    shop = Shop()
    assert _match(shop, shop_img)
    assert not _match(shop, pub_img)


def test_pub():
    pub = Pub()
    assert _match(pub, pub_img)
    assert not _match(pub, shop_img)


def test_forceswar():
    war_queue = ForcesWarQueue()
    war_exec = ForcesWarExec()
    assert _match(war_queue, forceswar_queue_img)
    assert not _match(war_queue, forceswar_exec_img)
    assert _match(war_exec, forceswar_exec_img)
    assert _match(war_exec, forceswar_exec2_img)
    assert not _match(war_exec, forceswar_queue_img)

    war_exec_s1 = ForcesWarExecStep1()
    war_exec_s2 = ForcesWarExecStep2()
    assert _match(war_exec_s1, forceswar_exec_img)
    assert _match(war_exec_s2, forceswar_exec2_img)

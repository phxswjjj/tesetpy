from datetime import datetime

import cv2

from inst.scene import FeatureRule
from inst.task.task_war import WarStepType, get_warstep

warstep1_prod_img = cv2.imread('inst/scene/img/test_warstep1_prod.jpg')
warstep1_prod2_img = cv2.imread('inst/scene/img/test_warstep1_prod2.jpg')
warstep2_fight_img = cv2.imread('inst/scene/img/test_warstep2_fight.jpg')


def test_war_time():
    assert get_warstep(datetime(2019, 6, 29, 16, 16)) == WarStepType.FIGHT
    assert get_warstep(datetime(2019, 6, 30, 16, 16)) == WarStepType.NONE


def test_warstep():
    rule_expand = FeatureRule('warstep_expand_building.jpg')
    assert not rule_expand.match(warstep1_prod_img)
    assert rule_expand.match(warstep1_prod2_img)
    assert not rule_expand.match(warstep2_fight_img)

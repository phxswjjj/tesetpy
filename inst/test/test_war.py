from datetime import datetime

import cv2

from inst.scene import FeatureRule
from inst.task.task_war import WarStepType, get_warstep

warstep1_prod_img = cv2.imread('inst/scene/img/test_warstep1_prod.jpg')
warstep1_prod2_img = cv2.imread('inst/scene/img/test_warstep1_prod2.jpg')
warstep1_prod3_img = cv2.imread('inst/scene/img/test_warstep1_prod3.jpg')
warstep1_prod4_img = cv2.imread('inst/scene/img/test_warstep1_prod4.jpg')
warstep2_fight_img = cv2.imread('inst/scene/img/test_warstep2_fight.jpg')
warstep2_fight2_img = cv2.imread('inst/scene/img/test_warstep2_fight2.jpg')
warstep2_select_img = cv2.imread('inst/scene/img/test_warstep2_select.jpg')
warstep2_select2_img = cv2.imread('inst/scene/img/test_warstep2_select2.jpg')
warstep2_select3_img = cv2.imread('inst/scene/img/test_warstep2_select3.jpg')


def test_war_time():
    assert get_warstep(datetime(2019, 6, 29, 16, 16)) == WarStepType.FIGHT
    assert get_warstep(datetime(2019, 6, 30, 16, 16)) == WarStepType.NONE


def test_warstep1():
    rule_expand = FeatureRule('warstep_expand_building.jpg')
    assert not rule_expand.match(warstep1_prod_img)
    assert rule_expand.match(warstep1_prod2_img)
    assert not rule_expand.match(warstep2_fight_img)

    rule_item_completed = FeatureRule('warstep1_item_completed.jpg')
    assert rule_item_completed.match(warstep1_prod3_img)
    assert not rule_item_completed.match(warstep1_prod4_img)

    rule_item_empty = FeatureRule('warstep_item_empty.jpg')
    assert not rule_item_empty.match(warstep1_prod3_img)
    assert rule_item_empty.match(warstep1_prod4_img)

    rule_war_completed = FeatureRule('warstep_completed.jpg')
    assert rule_war_completed.match(warstep1_prod_img)
    assert rule_war_completed.match(warstep1_prod2_img)


def test_warstep2():
    rule_war_completed = FeatureRule('warstep_completed.jpg')
    assert not rule_war_completed.match(warstep2_fight_img)
    assert not rule_war_completed.match(warstep2_fight2_img)

    rule_select_hard = FeatureRule('warstep2_select_hard.jpg')
    assert rule_select_hard.match(warstep2_fight_img)
    assert not rule_select_hard.match(warstep2_fight2_img)
    
    rule_select_role = FeatureRule('select_role.jpg', 0.9)
    assert rule_select_role.match(warstep2_select_img)
    assert rule_select_role.match(warstep2_select3_img)
    assert not rule_select_role.match(warstep2_select2_img)
    assert not rule_select_role.match(warstep2_fight_img)

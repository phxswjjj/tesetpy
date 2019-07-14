from datetime import datetime

import cv2

from inst.scene import FeatureRule
from inst.task.task_war import (TaskWarFight, TaskWarProduce, WarStepType,
                                get_warstep)

warstep1_prod_img = cv2.imread('inst/scene/img/test_warstep1_prod.jpg')
warstep1_prod2_img = cv2.imread('inst/scene/img/test_warstep1_prod2.jpg')
warstep1_prod3_img = cv2.imread('inst/scene/img/test_warstep1_prod3.jpg')
warstep1_prod4_img = cv2.imread('inst/scene/img/test_warstep1_prod4.jpg')
warstep1_prod5_img = cv2.imread('inst/scene/img/test_warstep1_prod5.jpg')
warstep1_prod6_img = cv2.imread('inst/scene/img/test_warstep1_prod6.jpg')
warstep1_prod7_img = cv2.imread('inst/scene/img/test_warstep1_prod7.jpg')
warstep1_prod8_img = cv2.imread('inst/scene/img/test_warstep1_prod8.jpg')
warstep1_prod9_img = cv2.imread('inst/scene/img/test_warstep1_prod9.jpg')
warstep2_start_img = cv2.imread('inst/scene/img/test_warstep2_start.jpg')
warstep2_fight_img = cv2.imread('inst/scene/img/test_warstep2_fight.jpg')
warstep2_fight2_img = cv2.imread('inst/scene/img/test_warstep2_fight2.jpg')
warstep2_fight3_img = cv2.imread('inst/scene/img/test_warstep2_fight3.jpg')
warstep2_select_img = cv2.imread('inst/scene/img/test_warstep2_select.jpg')
warstep2_select2_img = cv2.imread('inst/scene/img/test_warstep2_select2.jpg')
warstep2_select3_img = cv2.imread('inst/scene/img/test_warstep2_select3.jpg')
warstep2_return_img = cv2.imread('inst/scene/img/test_warstep2_return.jpg')
warstep2_repair_img = cv2.imread('inst/scene/img/test_warstep2_repair.jpg')
select_role_img = cv2.imread('inst/scene/img/test_select_role.jpg')


def test_war_time():
    assert get_warstep(datetime(2019, 6, 29, 16, 16)) == WarStepType.FIGHT
    assert get_warstep(datetime(2019, 6, 30, 16, 16)) == WarStepType.NONE


def test_warstep1():
    task = TaskWarProduce()

    rule_expand = FeatureRule('warstep_expand_building.jpg')
    assert not rule_expand.match(warstep1_prod_img)
    assert rule_expand.match(warstep1_prod2_img)
    assert not rule_expand.match(warstep2_fight_img)

    rule_item_completed = FeatureRule('warstep1_item_completed.jpg')
    assert rule_item_completed.match(warstep1_prod3_img)
    assert not rule_item_completed.match(warstep1_prod4_img)

    rule_item_upgrade_exit = FeatureRule('warstep1_upgrade_exit.jpg')
    assert not rule_item_upgrade_exit.match(warstep1_prod3_img)
    assert rule_item_upgrade_exit.match(warstep1_prod8_img)

    rule_item_empty = FeatureRule('warstep_item_empty.jpg')
    assert not rule_item_empty.match(warstep1_prod3_img)
    assert rule_item_empty.match(warstep1_prod4_img)

    rule_build = FeatureRule('warstep1_build.jpg')
    assert rule_build.match(warstep1_prod2_img)
    assert not rule_build.match(warstep1_prod3_img)

    rule_collect_res = FeatureRule('warstep1_collect_res.jpg')
    assert not rule_collect_res.match(warstep1_prod2_img)
    assert rule_collect_res.match(warstep1_prod6_img)
    
    rule_build2 = FeatureRule('warstep1_build2.jpg')
    assert not rule_build2.match(warstep1_prod2_img)
    assert rule_build2.match(warstep1_prod6_img)

    rule_submit = FeatureRule('warstep1_submit.jpg')
    assert not rule_submit.match(warstep1_prod2_img)
    assert rule_submit.match(warstep1_prod7_img)

    rule_submit_check = FeatureRule('warstep1_submit_check.jpg')
    assert not rule_submit_check.match(warstep1_prod2_img)
    assert rule_submit_check.match(warstep1_prod9_img)

    rule_submit2 = FeatureRule('warstep1_submit2.jpg')
    assert not rule_submit2.match(warstep1_prod2_img)
    assert rule_submit2.match(warstep1_prod9_img)

    rule_war_completed = task.get_rule_warstep_completed()
    assert rule_war_completed.match(warstep1_prod_img)
    assert rule_war_completed.match(warstep1_prod2_img)
    assert not rule_war_completed.match(warstep1_prod5_img)
    assert rule_war_completed.match(warstep1_prod6_img)


def test_warstep2():
    task = TaskWarFight()

    rule_start = FeatureRule('warstep2_start.jpg')
    assert rule_start.match(warstep2_start_img)
    assert not rule_start.match(warstep2_fight_img)

    rule_war_completed = task.get_rule_warstep_completed()
    assert not rule_war_completed.match(warstep2_fight_img)
    assert not rule_war_completed.match(warstep2_fight2_img)

    rule_select_hard = FeatureRule('warstep2_select_hard.jpg')
    assert rule_select_hard.match(warstep2_fight_img)
    assert not rule_select_hard.match(warstep2_fight2_img)

    rule_select_role_hard = FeatureRule('warstep2_select_role_hard.jpg')
    assert rule_select_role_hard.match(warstep2_select_img)
    assert rule_select_role_hard.match(warstep2_return_img)
    assert not rule_select_role_hard.match(select_role_img)

    rule_go = FeatureRule('warstep2_go.jpg')
    assert rule_go.match(warstep2_select_img)
    assert rule_go.match(warstep2_select2_img)
    assert rule_go.match(select_role_img)
    assert not rule_go.match(warstep2_return_img)

    rule_select_role = FeatureRule('select_role.jpg', 0.9)
    assert rule_select_role.match(warstep2_select_img)
    assert rule_select_role.match(warstep2_select3_img)
    assert not rule_select_role.match(warstep2_select2_img)
    assert not rule_select_role.match(warstep2_fight_img)

    rule_power40 = FeatureRule('select_role_power40.jpg', 0.90)
    assert not rule_power40.match(warstep2_select_img)
    assert not rule_power40.match(warstep2_select3_img)
    assert rule_power40.match(warstep2_select2_img)
    assert not rule_power40.match(warstep2_fight_img)
    assert rule_power40.match(select_role_img)

    rule_wait_return = task.get_rule_wait_return()
    assert rule_wait_return.match(warstep2_fight2_img)
    assert not rule_wait_return.match(warstep1_prod2_img)
    
    rule_return = FeatureRule('warstep2_return.jpg')
    assert not rule_return.match(warstep2_fight2_img)
    assert rule_return.match(warstep2_fight3_img)

    rule_repair = FeatureRule('warstep2_submit.jpg')
    assert rule_repair.match(warstep2_repair_img)
    assert not rule_repair.match(warstep2_fight3_img)

    rule_close = FeatureRule('warstep2_close.jpg')
    assert not rule_close.match(warstep2_fight2_img)
    assert rule_close.match(warstep2_return_img)

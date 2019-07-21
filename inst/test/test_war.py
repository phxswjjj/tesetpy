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

    rule_expand = task.get_rule_expand_building()
    assert not rule_expand.match(warstep1_prod_img)
    assert rule_expand.match(warstep1_prod2_img)
    assert not rule_expand.match(warstep2_fight_img)

    rule_item_completed = task.get_rule_item_completed()
    assert rule_item_completed.match(warstep1_prod3_img)
    assert not rule_item_completed.match(warstep1_prod4_img)

    rule_item_upgrade_exit = task.get_rule_upgrade_exit()
    assert not rule_item_upgrade_exit.match(warstep1_prod3_img)
    assert rule_item_upgrade_exit.match(warstep1_prod8_img)

    rule_item_empty = task.get_rule_item_empty()
    assert not rule_item_empty.match(warstep1_prod3_img)
    assert rule_item_empty.match(warstep1_prod4_img)

    rule_build = task.get_rule_build_open()
    assert rule_build.match(warstep1_prod2_img)
    assert not rule_build.match(warstep1_prod3_img)

    rule_collect_res = task.get_rule_colllect_res()
    assert not rule_collect_res.match(warstep1_prod2_img)
    assert rule_collect_res.match(warstep1_prod6_img)
    
    rule_build2 = task.get_rule_build_confirm()
    assert not rule_build2.match(warstep1_prod2_img)
    assert rule_build2.match(warstep1_prod6_img)

    rule_submit = task.get_rule_item_submit()
    assert not rule_submit.match(warstep1_prod2_img)
    assert rule_submit.match(warstep1_prod7_img)

    rule_submit_check = task.get_rule_item_submit_check()
    assert not rule_submit_check.match(warstep1_prod2_img)
    assert rule_submit_check.match(warstep1_prod9_img)

    rule_submit2 = task.get_rule_item_submit2()
    assert not rule_submit2.match(warstep1_prod2_img)
    assert rule_submit2.match(warstep1_prod9_img)

    rule_war_completed = task.get_rule_warstep_completed()
    assert rule_war_completed.match(warstep1_prod_img)
    assert rule_war_completed.match(warstep1_prod2_img)
    assert not rule_war_completed.match(warstep1_prod5_img)
    assert not rule_war_completed.match(warstep1_prod6_img)


def test_warstep2():
    task = TaskWarFight()

    rule_start = task.get_rule_start()
    assert rule_start.match(warstep2_start_img)
    assert not rule_start.match(warstep2_fight_img)

    rule_war_completed = task.get_rule_warstep_completed()
    assert rule_war_completed.match(warstep2_fight_img)
    assert not rule_war_completed.match(warstep2_fight2_img)

    rule_select_hard = task.get_rule_select_hardmode()
    assert rule_select_hard.match(warstep2_fight_img)
    assert not rule_select_hard.match(warstep2_fight2_img)

    rule_select_role_hard = task.get_rule_selectrole_hardmode()
    assert rule_select_role_hard.match(warstep2_select_img)
    assert rule_select_role_hard.match(warstep2_return_img)
    assert not rule_select_role_hard.match(select_role_img)

    rule_go = task.get_rule_fight_go()
    assert rule_go.match(warstep2_select_img)
    assert rule_go.match(warstep2_select2_img)
    assert rule_go.match(select_role_img)
    assert not rule_go.match(warstep2_return_img)

    rule_select_role = task.get_rule_selectrole()
    assert rule_select_role.match(warstep2_select_img)
    assert rule_select_role.match(warstep2_select3_img)
    assert not rule_select_role.match(warstep2_select2_img)
    assert not rule_select_role.match(warstep2_fight_img)

    rule_power40 = task.get_rule_selectrole_power40()
    assert not rule_power40.match(warstep2_select_img)
    assert not rule_power40.match(warstep2_select3_img)
    assert rule_power40.match(warstep2_select2_img)
    assert not rule_power40.match(warstep2_fight_img)
    assert rule_power40.match(select_role_img)

    rule_wait_return = task.get_rule_wait_return()
    assert rule_wait_return.match(warstep2_fight2_img)
    assert not rule_wait_return.match(warstep1_prod2_img)
    
    rule_return = task.get_rule_fight_return()
    assert not rule_return.match(warstep2_fight2_img)
    assert rule_return.match(warstep2_fight3_img)

    rule_repair = task.get_rule_repair()
    assert rule_repair.match(warstep2_repair_img)
    assert not rule_repair.match(warstep2_fight3_img)

    rule_close = task.get_rule_fight_completed_close()
    assert not rule_close.match(warstep2_fight2_img)
    assert rule_close.match(warstep2_return_img)

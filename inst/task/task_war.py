import time
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from enum import Enum, unique

from ..scene import FeatureRule
from ..scene.forces import ForcesWarExecStep1, ForcesWarExecStep2
from . import TaskBase, TaskWnd

# 第一次進行戰爭籌備時間(參考基準)
warstep_first_prod_date = datetime(2019, 3, 11, 9)


@unique
class WarStepType(Enum):
    NONE = 0
    PROD = 1
    FIGHT = 2


def get_warstep(t: datetime = datetime.now()) -> WarStepType:
    global warstep_first_prod_date
    wstep = WarStepType.NONE

    now = t
    dif_hour = (now - warstep_first_prod_date).total_seconds()/60/60 % 168 % 84

    if dif_hour < 24:
        wstep = WarStepType.PROD
    elif dif_hour < 36:
        pass
    elif dif_hour < 60:
        wstep = WarStepType.FIGHT

    return wstep


class TaskWarBase(TaskBase, metaclass=ABCMeta):
    @abstractmethod
    def run(self, w: TaskWnd):
        return NotImplemented

    def _go_war(self, w: TaskWnd):
        pass

    def get_rule_warstep_completed(self) -> FeatureRule:
        return FeatureRule('warstep_completed.jpg', 0.98)


class TaskWarFight(TaskWarBase):
    def __init__(self):
        self._last_run_time: datetime = None
        self._wait_time: datetime = None

    def run(self, w: TaskWnd):
        wstep = get_warstep()
        if wstep != WarStepType.FIGHT:
            return

        if self._last_run_time:
            dif: timedelta = datetime.now() - self._last_run_time
            if dif < timedelta(0, 30*60, 0):
                return

        if self._wait_time:
            if datetime.now() < self._wait_time:
                return
            else:
                self._wait_time = None

        self._go_war(w)
        self._fight(w)

    def _go_war(self, w: TaskWnd):
        super()._go_war(w)

    def _fight(self, w: TaskWnd):
        if w.is_scene(ForcesWarExecStep2):
            # 戰鬥結束
            rule_war_completed = self.get_rule_warstep_completed()
            if w.match_rules([rule_war_completed]):
                self._wait_time = datetime.now() + timedelta(1)
                return

            # 選擇 Hard mode
            rule_select_hard = FeatureRule('warstep2_select_hard.jpg')
            if w.match_rules([rule_select_hard]):
                w.mouse_left_click(rule_select_hard.loc_last_result)
                time.sleep(0.5)

            # 選擇角色出戰
            rule_select_role_hard = FeatureRule(
                'warstep2_select_role_hard.jpg')
            rule_go = FeatureRule('warstep2_go.jpg')
            if w.match_rules([rule_select_role_hard, rule_go]):
                # 選擇隊伍
                rule_select_role = FeatureRule('select_role.jpg', 0.9)
                rule_power40 = FeatureRule('select_role_power40.jpg', 0.95)
                for i in range(8):
                    select_group_key = i + 1
                    w.key_press(str(i))
                    time.sleep(0.5)

                    w.refresh_screen()
                    if not w.match_rules([rule_select_role]) and w.match_rules([rule_power40, rule_go]):
                        w.mouse_left_click(rule_go.loc_last_result)
                        self._last_run_time = datetime.now()
                        return

            # 戰鬥完成
            rule_wait_return = self.get_rule_wait_return()
            if w.match_rules([rule_wait_return]):
                self._wait_time = datetime.now() + timedelta(0, 10*60)
                return
            else:
                pass

    def get_rule_wait_return(self) -> FeatureRule:
        return FeatureRule('warstep2_wait_return.jpg')


class TaskWarProduce(TaskWarBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        pass

        self._go_war(w)
        self._produce(w)

    def _go_war(self, w: TaskWnd):
        super()._go_war(w)

    def _produce(self, w: TaskWnd):
        if w.is_scene(ForcesWarExecStep1):
            # 壽備結束
            rule_war_completed = self.get_rule_warstep_completed()
            if w.match_rules([rule_war_completed]):
                self._wait_time = datetime.now() + timedelta(1)
                return

            rule_expand = FeatureRule('warstep_expand_building.jpg')
            if w.match_rules([rule_expand]):
                # 打開建造中道具列表
                w.mouse_left_click(rule_expand.loc_last_result)
                time.sleep(0.5)
                w.refresh_screen()

            # 收成
            rule_item_completed = FeatureRule('warstep1_item_completed.jpg')
            for i in range(6):
                if w.match_rules([rule_item_completed]):
                    w.mouse_left_click(rule_item_completed.loc_last_result)
                    time.sleep(0.5)
                    w.refresh_screen()

            # 提交
            rule_submit = FeatureRule('warstep1_submit.jpg')
            for i in range(3):
                if w.match_rules([rule_submit]):
                    w.mouse_left_click(rule_submit.loc_last_result)
                    time.sleep(0.5)
                    w.refresh_screen()

            # 建造
            rule_item_empty = FeatureRule('warstep_item_empty.jpg')
            rule_build = FeatureRule('warstep1_build.jpg')
            rule_build2 = FeatureRule('warstep1_build2.jpg')
            rule_collect_res = FeatureRule('warstep1_collect_res.jpg')
            for i in range(6):
                if w.match_rules([rule_item_empty, rule_build]):
                    w.mouse_left_click(rule_build.loc_last_result)
                    time.sleep(0.5)
                    w.refresh_screen()
                    if w.match_rules([rule_collect_res, rule_build2]):
                        w.mouse_left_click(rule_collect_res.loc_last_result)
                        time.sleep(0.2)
                        w.mouse_left_click(rule_build2.loc_last_result)
                        time.sleep(0.5)
                        w.refresh_screen()

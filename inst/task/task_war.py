import time
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from enum import Enum, unique

from ..scene import FeatureRule
from ..scene.forces import (ForcesWarExecStep1, ForcesWarExecStep2,
                            ForcesWarQueue)
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
        """特徵-籌備/戰鬥達到目標
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep_completed.jpg', 0.993)


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

        w.refresh_scene()
        self._go_war(w)
        self._fight(w)

    def _go_war(self, w: TaskWnd):
        super()._go_war(w)
        if w.is_scene(ForcesWarQueue):
            rule_start = self.get_rule_start()
            if w.match_rules([rule_start]):
                w.mouse_left_click(rule_start.loc_last_result)
                time.sleep(0.5)
                w.refresh_scene()

    def _fight(self, w: TaskWnd):
        if w.is_scene(ForcesWarExecStep2):
            # 戰鬥結束
            rule_war_completed = self.get_rule_warstep_completed()
            if w.match_rules([rule_war_completed]):
                self._wait_time = datetime.now() + timedelta(1)
                return

            # 選擇 Hard mode
            rule_select_hard = self.get_rule_select_hardmode()
            if w.match_rules([rule_select_hard]):
                w.mouse_left_click(rule_select_hard.loc_last_result)
                time.sleep(0.5)
                w.refresh_screen()

            # 選擇角色出戰
            rule_select_role_hard = self.get_rule_selectrole_hardmode()
            rule_go = self.get_rule_fight_go()
            if w.match_rules([rule_select_role_hard, rule_go]):
                # 選擇隊伍
                rule_select_role = self.get_rule_selectrole()
                rule_power40 = self.get_rule_selectrole_power40()
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
                rule_return = self.get_rule_fight_return()
                if w.match_rules([rule_return]):
                    w.mouse_left_click(rule_return.loc_last_result)
                    time.sleep(0.5)

                    for _ in range(2):
                        w.key_press('f')
                        time.sleep(0.3)

                    w.refresh_screen()
                    rule_repair = self.get_rule_repair()
                    if w.match_rules([rule_repair]):
                        w.mouse_left_click(rule_repair.loc_last_result)
                        time.sleep(0.3)
                        w.refresh_screen()

                    rule_close = self.get_rule_fight_completed_close()
                    if w.match_rules([rule_close]):
                        w.mouse_left_click(rule_close.loc_last_result)
                        time.sleep(0.5)
                    else:
                        print('not found close')

    def get_rule_start(self) -> FeatureRule:
        return FeatureRule('warstep2_start.jpg')

    def get_rule_select_hardmode(self) -> FeatureRule:
        """特徵-選擇困難模式

        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_select_hard.jpg')

    def get_rule_selectrole_hardmode(self) -> FeatureRule:
        """特徵-困難模式下選擇角色
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_select_role_hard.jpg')

    def get_rule_selectrole(self) -> FeatureRule:
        """特徵-文字: 選擇角色，有這文字表示選角未湊滿不可出戰，只適用 5 人隊
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('select_role.jpg', 0.9)

    def get_rule_selectrole_power40(self) -> FeatureRule:
        """特徵-選擇角色後，滿 5 人戰力加成 40%
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('select_role_power40.jpg', 0.9)

    def get_rule_fight_go(self) -> FeatureRule:
        """特徵-選完角色並進行戰鬥(GO)
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_go.jpg')

    def get_rule_wait_return(self) -> FeatureRule:
        """特徵-等待戰鬥完成

        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_wait_return.jpg')

    def get_rule_fight_return(self) -> FeatureRule:
        """特徵-戰鬥完成

        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_return.jpg')

    def get_rule_repair(self) -> FeatureRule:
        """特徵-同意(確定)修裝

        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_submit.jpg')

    def get_rule_fight_completed_close(self) -> FeatureRule:
        """特徵-戰鬥完成，關閉結算畫面

        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep2_close.jpg')


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
            # 籌備結束
            rule_war_completed = self.get_rule_warstep_completed()
            if w.match_rules([rule_war_completed]):
                self._wait_time = datetime.now() + timedelta(1)
                return

            rule_expand = self.get_rule_expand_building()
            if w.match_rules([rule_expand]):
                # 打開建造中道具列表
                w.mouse_left_click(rule_expand.loc_last_result)
                time.sleep(0.5)
                w.refresh_screen()

            # 收成
            rule_item_completed = self.get_rule_item_completed()
            rule_item_upgrade_exit = self.get_rule_upgrade_exit()
            for i in range(6):
                if w.match_rules([rule_item_completed]):
                    w.mouse_left_click(rule_item_completed.loc_last_result)
                    time.sleep(0.5)
                    w.refresh_screen()
                    if w.match_rules([rule_item_upgrade_exit]):
                        w.mouse_left_click(
                            rule_item_upgrade_exit.loc_last_result)
                        time.sleep(0.3)
                        w.refresh_screen()

            # 提交
            rule_submit = self.get_rule_item_submit()
            rule_submit_check = self.get_rule_item_submit_check()
            rule_submit2 = self.get_rule_item_submit2()
            for i in range(3):
                if w.match_rules([rule_submit]):
                    w.mouse_left_click(rule_submit.loc_last_result)
                    time.sleep(0.5)
                    w.refresh_screen()
                    if w.match_rules([rule_submit_check, rule_submit2]):
                        w.mouse_left_click(rule_submit2.loc_last_result)
                        time.sleep(0.3)
                        w.refresh_screen()

            # 建造
            rule_item_empty = self.get_rule_item_empty()
            rule_build = self.get_rule_build_open()
            rule_build2 = self.get_rule_build_confirm()
            rule_collect_res = self.get_rule_colllect_res()
            for i in range(6):
                if w.match_rules([rule_item_empty, rule_build]):
                    w.mouse_left_click(rule_build.loc_last_result)
                    time.sleep(0.2)
                    w.refresh_screen()
                    if w.match_rules([rule_collect_res, rule_build2]):
                        w.mouse_left_click(rule_collect_res.loc_last_result)
                        time.sleep(0.2)
                        w.mouse_left_click(rule_build2.loc_last_result)
                        time.sleep(0.5)
                        w.refresh_screen()
                    else:
                        rule_build_cancel = self.get_rule_build_cancel()
                        rule_build_nores = self.get_rule_build_nores()
                        if w.match_rules([rule_build_cancel, rule_build_nores]):
                            w.mouse_left_click(rule_build_cancel.loc_last_result)
                            self._wait_time = datetime.now() + timedelta(0, 5*60)
                            return

    def get_rule_expand_building(self) -> FeatureRule:
        """特徵-展開製作中的道具列表
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep_expand_building.jpg')

    def get_rule_item_completed(self) -> FeatureRule:
        """特徵-道具製作完成
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_item_completed.jpg')

    def get_rule_upgrade_exit(self) -> FeatureRule:
        """特徵-取消道具升階
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_upgrade_exit.jpg')

    def get_rule_item_empty(self) -> FeatureRule:
        """特徵-空的製作欄
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep_item_empty.jpg')

    def get_rule_build_open(self) -> FeatureRule:
        """特徵-開啟道具製作確認視窗
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_build.jpg')

    def get_rule_colllect_res(self) -> FeatureRule:
        """特徵-收集資源
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_collect_res.jpg')

    def get_rule_build_confirm(self) -> FeatureRule:
        """特徵-執行道具製作
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_build2.jpg')

    def get_rule_build_nores(self) -> FeatureRule:
        """特徵-無資源改用鑽石製作
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_build_nores.jpg')

    def get_rule_build_cancel(self) -> FeatureRule:
        """特徵-取消執行道具製作
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_build_cancel.jpg')

    def get_rule_item_submit(self) -> FeatureRule:
        """特徵-提交道具
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_submit.jpg')

    def get_rule_item_submit_check(self) -> FeatureRule:
        """特徵-提交道具含有稀有物品，確認是否提交
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_submit_check.jpg')

    def get_rule_item_submit2(self) -> FeatureRule:
        """特徵-確定提交稀有道具
        
        Returns:
            FeatureRule -- [description]
        """
        return FeatureRule('warstep1_submit2.jpg')

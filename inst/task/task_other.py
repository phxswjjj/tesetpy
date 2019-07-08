import operator
import time
from datetime import datetime, timedelta

from ..scene import FeatureRule
from . import TaskBase, TaskWnd


class TaskReconnect(TaskBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        if not w.cur_scene:
            rule_reconnect = FeatureRule('reconnect.jpg', 0.9)
            if w.match_rules([rule_reconnect]):
                loc_reconnect = rule_reconnect.loc_last_result
                w.mouse_left_click(loc_reconnect)

                sleep_sec: int = 10
                if self._last_run_time:
                    dif: timedelta = datetime.now() - self._last_run_time
                    # 10 min 內又斷線，等 30 min 再試
                    if dif < timedelta(0, 10*60, 0):
                        sleep_sec = 30*60
                self._last_run_time = datetime.now()
                time.sleep(sleep_sec)


class TaskSelectServer(TaskBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        if self._last_run_time:
            dif: timedelta = datetime.now() - self._last_run_time
            # 2 hr 內不重試，可能伺服器維修
            if dif < timedelta(0, 2*60*60, 0):
                return

        if not w.cur_scene:
            rule_enter = FeatureRule('select_server_enter.jpg', 0.9)
            if w.match_rules([rule_enter]):
                self._last_run_time = datetime.now()
                loc = rule_enter.loc_last_result
                w.mouse_left_click(loc)
                time.sleep(5)

                # close ad
                w.refresh_screen()
                rule_close = FeatureRule('shop_close.jpg')
                if w.match_rules([rule_close]):
                    w.mouse_left_click(rule_close.loc_last_result)
                    time.sleep(0.5)
        else:
            # 有其他場景視為已執行過
            self._last_run_time = datetime.now()

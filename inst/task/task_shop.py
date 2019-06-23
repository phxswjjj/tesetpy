import operator
from datetime import datetime, timedelta

from ..scene import FeatureRule
from ..scene.shop import Shop
from . import TaskBase, TaskWnd


class TaskCollectResource(TaskBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        if self._last_run_time:
            dif: timedelta = datetime.now() - self._last_run_time
            if dif < timedelta(0, 30*60, 0):
                return

        if w.is_scene(Shop):
            self._last_run_time = datetime.now()
            rule_stone = FeatureRule('shop_res_stone.jpg', 0.9)
            rule_magic = FeatureRule('shop_res_magic.jpg')
            if w.match_rules([rule_stone, rule_magic]):
                loc_stone = rule_stone.loc_last_result
                loc_magic = rule_magic.loc_last_result
                # 最後一個項目要移動才會觸發，增加 offset
                loc_magic = tuple(map(operator.add, loc_magic, (0, 30)))
                w.mouse_move(loc_stone, loc_magic, 500)

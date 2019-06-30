import time
from datetime import datetime, timedelta
from enum import Enum, unique

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


class TaskWarFight(TaskBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        pass


class TaskWarProduce(TaskBase):
    def __init__(self):
        self._last_run_time: datetime = None

    def run(self, w: TaskWnd):
        pass

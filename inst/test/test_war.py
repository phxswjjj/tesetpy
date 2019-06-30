from datetime import datetime

from inst.task.task_war import WarStepType, get_warstep


def test_war_time():
    assert get_warstep(datetime(2019, 6, 29, 16, 16)) == WarStepType.FIGHT
    assert get_warstep(datetime(2019, 6, 30, 16, 16)) == WarStepType.NONE

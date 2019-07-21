import math
import os
import time

import keyboard
from pymouse import PyMouse

from .cadria import wnd
from .scene.forces import (ForcesWarExecStep1, ForcesWarExecStep2,
                           ForcesWarQueue)
from .scene.pub import Pub
from .scene.shop import Shop
from .task import task_other, task_shop, task_war


def main():
    keyboard.add_hotkey('esc', stop_task)
    print('press esc anywhere to stop this script')

    tasks = [
        task_war.TaskWarFight(),
        task_war.TaskWarProduce(),
        task_shop.TaskCollectResource(),
        task_other.TaskReconnect(),
        task_other.TaskSelectServer()
    ]

    w = wnd()
    if not w.load():
        os.startfile('steam://rungameid/883860')
        time.sleep(2)
        
    for i in range(10):
        if not w.load():
            print('cadria load fail, retry({})...'.format(i))
            time.sleep(2)
        else:
            break

    if not w.load():
        print('cadria load fail, exit...')
        return

    mouse = PyMouse()
    while True:
        # 電腦操作中暫停執行
        p1 = mouse.position()
        time.sleep(1)
        p2 = mouse.position()
        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        if dist > 10 and False:
            print('電腦操作中暫停執行', dist)
            time.sleep(600)
            print('從暫停恢復執行')
            continue

        for task in tasks:
            task.run(w)
        time.sleep(10)


def stop_task():
    print('STOP TASK')
    import os
    os._exit(1)


if __name__ == '__main__':
    main()

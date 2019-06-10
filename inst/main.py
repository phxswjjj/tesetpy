import time

import keyboard

from .cadria import wnd
from .scene.pub import Pub
from .scene.shop import Shop
from .task import task_war


def main():
    keyboard.add_hotkey('esc', stop_task)
    print('press esc anywhere to stop this script')

    tasks = [
        task_war.TaskWarFight(),
        task_war.TaskWarProduce()
    ]

    w = wnd()
    if not w.load():
        print('cadria load fail')
        return

    while True:
        if w.identify_scene():
            print(w.cur_scene.__class__.__name__)
        time.sleep(2)


def stop_task():
    print('STOP TASK')
    import os
    os._exit(1)


if __name__ == '__main__':
    main()

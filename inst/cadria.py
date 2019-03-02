from .win32 import wnd as wnd32
import time

class WarFightMode:
    EASY = 0
    MEDIUM = 1
    HARD = 2

class wnd(wnd32):
    __defaultsize = (1606, 925)

    def __init__(self):
        super().__init__()
        self.sizeratio = (1, 1)

    def load(self):
        super().load('Cadria Item Shop')

        defaultsize = wnd.__defaultsize
        size = self.size
        self.sizeratio = (size[0] / defaultsize[0], size[1] / defaultsize[1])

    def click(self, rx, ry, button = 1, n = 1):
        sizeratio = self.sizeratio
        rx = int(round(rx * sizeratio[0]))
        ry = int(round(ry * sizeratio[1]))
        super().click(rx, ry, button, n)

    def warProduce(self):
        rx, ry = (420, 320)
        self.click_l(rx, ry)

        time.sleep(1)
        rx, ry = (1100, 750)
        self.click_l(rx, ry)

    def warHarvest(self, posSeq):
        # posSeq: 0~5
        rx, ry = (1100 + posSeq*90, 850)
        self.click_l(rx, ry)
        time.sleep(1)
        self.__warUpgradeCancel()
    
    def __warUpgradeCancel(self):
        rx, ry = (700, 790)
        self.click_l(rx, ry)

    def warFight(self, teamNo, mode=WarFightMode.HARD):
        # teamNo: 1~7
        rx, ry = (390 + mode*200, 490)
        self.click_l(rx, ry)
        time.sleep(0.5)

        self.tap(teamNo)
        time.sleep(0.5)

        self.tap('g')

    def warFightCompleted(self):
        rx, ry = (590, 490)
        self.click_l(rx, ry)
        time.sleep(0.5)

        self.tap('g')
        time.sleep(0.5)
        rx, ry = (940, 710)
        self.click_l(rx, ry)
        
        time.sleep(2)
        
        rx, ry = (1430, 140)
        self.click_l(rx, ry)

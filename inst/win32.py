import win32gui
import win32con
from PIL import ImageGrab
from pymouse import PyMouse
from pykeyboard import PyKeyboard

class wnd:
    def __init__(self):
        self.hwnd = None
        self.rect = None
        self.size = None
        self.image = None
        self.m = PyMouse()
        self.k = PyKeyboard()

    def load(self, wintitle):
        self.hwnd = win32gui.FindWindow(None, wintitle)
        rect = win32gui.GetWindowRect(self.hwnd)
        self.rect = rect

        size = (rect[2] - rect[0], rect[3] - rect[1])
        self.size = size

    def grab(self):
        self.focus()

        rect = self.rect
        self.image = ImageGrab.grab(rect)

    def focus(self):
        hwnd = self.hwnd

        if(win32gui.GetForegroundWindow() != hwnd):
            if(not win32gui.IsIconic(hwnd)):
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    def abspos(self, x, y):
        rect = self.rect

        return (rect[0] + x, rect[1] + y)

    def click(self, rx, ry, button = 1, n = 1):
        rect = self.rect
        x, y = rect[0] + rx, rect[1] + ry
        self.m.click(x, y, button, n)

    def click_l(self, rx, ry, n = 1):
        self.click(rx, ry, n)

    def tap(self, c, n = 1):
        self.k.tap_key(c, n)
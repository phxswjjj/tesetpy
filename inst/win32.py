import win32gui
import win32con
import win32gui
from PIL import ImageGrab
from pykeyboard import PyKeyboard
from pymouse import PyMouse

from .types import Position


class wrect:
    def __init__(self, *args, **kwargs):
        '''
        :param args: (left: int, top: int, right: int, bottom: int)
        :param kwargs: pos1=(left: int, top: int) or Position, pos2=(right: int, bottom: int) or Position
        '''
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

        if len(args) != 0 and len(args) != 4:
            raise ValueError('len of *args must 4')
        elif len(args) == 4:
            self.left, self.top, self.right, self.bottom = args
        else:
            for key, value in kwargs.items():
                if key == 'pos1':
                    if isinstance(value, Position):
                        self.left, self.top = value.x, value.y
                    else:
                        self.left, self.top = value
                elif key == 'pos2':
                    if isinstance(value, Position):
                        self.right, self.bottom = value.x, value.y
                    else:
                        self.right, self.bottom = value
                else:
                    setattr(self, key, value)

        # switch
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.bottom > self.top:
            self.top, self.bottom = self.bottom, self.top

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.left, self.top, self.right, self.bottom) == other
        else:
            return super().__eq__(other)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.left, self.top, self.right, self.bottom)


class wsize:
    def __init__(self, *args, **kwargs):
        self.width = 0
        self.height = 0

        if len(args) != 0 and len(args) != 2 and len(args) != 4:
            raise ValueError('len of *args must 2 or 4')
        elif len(args) == 2:
            self.width, self.height = args
        elif len(args) == 4:
            # args=(left, top, right, bottom)
            self.width, self.height = args[2] - args[0], args[3] - args[1]
        else:
            pos1: Position = None
            pos2: Position = None
            for key, value in kwargs.items():
                if key == 'size':
                    self.width, self.height = value
                elif key == 'pos1':
                    if isinstance(value, Position):
                        pos1 = value
                    else:
                        pos1 = Position(*value)
                elif key == 'pos2':
                    if isinstance(value, Position):
                        pos2 = value
                    else:
                        pos2 = Position(*value)
                else:
                    setattr(self, key, value)
            if pos1 == None and pos2 == None:
                pass
            elif pos1 == None or pos2 == None:
                raise ValueError('pos1 or pos2 is None')
            else:
                self.width = abs(pos1.x - pos2.x)
                self.height = abs(pos1.y - pos2.y)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.width, self.height) == other
        else:
            return super().__eq__(other)

    def __str__(self):
        return '({}, {})'.format(self.width, self.height)


class wnd:
    def __init__(self):
        self.hwnd = 0
        # (left, top, right, bottom)
        self.rect = (0, 0, 0, 0)
        # (width, height)
        self.size = (0, 0)
        self.image = None
        self.m = PyMouse()
        self.k = PyKeyboard()

    def load(self, wintitle):
        '''
        find window by title, calculate window rect and size
        '''
        hwnd = win32gui.FindWindow(None, wintitle)
        self.hwnd = hwnd

        # 最小化會無法取得 window rect
        if(win32gui.IsIconic(hwnd)):
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        rect = win32gui.GetWindowRect(hwnd)
        self.rect = rect

        size = (rect[2] - rect[0], rect[3] - rect[1])
        self.size = size

    def grab(self):
        '''
        take a screenshot of window
        '''
        self.focus()

        rect = self.rect
        self.image = ImageGrab.grab(rect)

    def focus(self):
        '''
        bring a window foreground
        '''
        hwnd = self.hwnd

        if(win32gui.GetForegroundWindow() != hwnd):
            if(not win32gui.IsIconic(hwnd)):
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    def abspos(self, x, y):
        rect = self.rect

        return (rect[0] + x, rect[1] + y)

    def click(self, rx, ry, button=1, n=1):
        rect = self.rect
        x, y = rect[0] + rx, rect[1] + ry
        self.m.click(x, y, button, n)

    def click_l(self, rx, ry, n=1):
        self.click(rx, ry, n)

    def tap(self, c, n=1):
        self.k.tap_key(c, n)

    def minimize(self):
        hwnd = self.hwnd

        if(win32gui.GetForegroundWindow() == hwnd):
            if(not win32gui.IsIconic(hwnd)):
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

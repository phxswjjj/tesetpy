import collections
import time

import numpy as np
import win32con
import win32gui
from PIL import ImageGrab
from pykeyboard import PyKeyboard
from pymouse import PyMouse

from .types import ITuple


def _itr_to_tup(itr: collections.Iterable, mul: int):
    return tuple(mul * i for i in itr)


class wpos(ITuple):
    """座標位置(x, y)"""

    def __init__(self, *args, **kwargs):
        """
        :param args: x, y
        :param kwargs: x, y
        """
        self.x = 0
        self.y = 0

        if args and len(args) != 2:
            raise ValueError('len of {} must 2'.format(args))
        elif len(args) == 2:
            self.x, self.y = args
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __add__(self, other):
        if isinstance(other, int):
            return wpos(self.x + other, self.y + other)
        elif isinstance(other, wpos):
            return wpos(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            if len(other) == 2:
                return self + wpos(*other)
            else:
                raise ValueError('len of {} must 2'.format(other))
        else:
            raise ValueError('{} type not support'.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, collections.Iterable):
            return self.__add__(tuple(-1 * i for i in other))
        else:
            return self.__add__(-1 * other)

    def totup(self):
        return (self.x, self.y)


class wrect(ITuple):
    def __init__(self, *args, **kwargs):
        '''
        :param args: (left: int, top: int, right: int, bottom: int)
        :param kwargs: pos1=(left: int, top: int), pos2=(right: int, bottom: int)
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
                    self.left, self.top = value
                elif key == 'pos2':
                    self.right, self.bottom = value
                else:
                    setattr(self, key, value)

        # switch
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.bottom > self.top:
            self.top, self.bottom = self.bottom, self.top

    def totup(self):
        return (self.left, self.top, self.right, self.bottom)

    def __add__(self, other):
        if isinstance(other, int):
            return wrect(*(i + other for i in self.totup()))
        elif isinstance(other, tuple):
            if len(other) == 2:
                o = other * 2
            elif len(other) == 4:
                o = other
            else:
                raise ValueError('len of {} must 2 or 4'.format(other))
            a = []
            for i, v in enumerate(self.totup()):
                a.append(o[i] + v)
            return wrect(*a)
        else:
            raise ValueError('{} type not support'.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, collections.Iterable):
            return self.__add__(tuple(-1 * i for i in other))
        else:
            return self.__add__(-1 * other)

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.left, self.top, self.right, self.bottom)


class wsize(ITuple):
    def __init__(self, *args, **kwargs):
        """
        :param args:
            width, height
            left, top, right, bottom
            (x1, y1), (x2, y2)
        :param kwargs:
            width,
            height,
            size=(width, height),
            pos1=(x1, y1) or wpos,
            pos2=(x2, y2) or wpos
        """
        self.width = 0
        self.height = 0

        if len(args) != 0 and len(args) != 2 and len(args) != 4:
            raise ValueError('len of *args must 2 or 4')
        elif len(args) == 2:
            p1, p2 = args
            if isinstance(p1, tuple) and len(p1) != 2:
                raise ValueError('must tuple[int, int]: {}'.format(p1))
            elif isinstance(p2, tuple) and len(p2) != 2:
                raise ValueError('must tuple[int, int]: {}'.format(p2))
            elif isinstance(p1, tuple) and isinstance(p2, tuple):
                x1, y1 = p1
                x2, y2 = p2
                self.width, self.height = abs(x2 - x1), abs(y2 - y1)
            else:
                self.width, self.height = args
        elif len(args) == 4:
            # args=(left, top, right, bottom)
            self.width, self.height = abs(
                args[2] - args[0]), abs(args[3] - args[1])
        else:
            pos1: wpos = None
            pos2: wpos = None
            for key, value in kwargs.items():
                if key == 'size':
                    self.width, self.height = value
                elif key == 'pos1':
                    if isinstance(value, wpos):
                        pos1 = value
                    else:
                        pos1 = wpos(*value)
                elif key == 'pos2':
                    if isinstance(value, wpos):
                        pos2 = value
                    else:
                        pos2 = wpos(*value)
                else:
                    setattr(self, key, value)
            if pos1 == None and pos2 == None:
                pass
            elif pos1 == None or pos2 == None:
                raise ValueError('pos1 or pos2 is None')
            else:
                self.width = abs(pos1.x - pos2.x)
                self.height = abs(pos1.y - pos2.y)

        if self.width < 0 or self.height < 0:
            raise ValueError('width or height must >= 0')

    def totup(self):
        return (self.width, self.height)

    def __add__(self, other):
        if isinstance(other, int):
            return wsize(*(i + other for i in self.totup()))
        elif isinstance(other, tuple):
            if len(other) == 2:
                o = other
            else:
                raise ValueError('len of {} must 2'.format(other))
            a = []
            for i, v in enumerate(self.totup()):
                a.append(o[i] + v)
            return wsize(*a)
        elif isinstance(other, wsize):
            return self.__add__(other.totup())
        else:
            raise ValueError('{} type not support'.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, collections.Iterable):
            return self.__add__(_itr_to_tup(other, -1))
        elif isinstance(other, wsize):
            return self.__add__(_itr_to_tup(other.totup(), -1))
        else:
            return self.__add__(-1 * other)

    def __str__(self):
        return '({}, {})'.format(self.width, self.height)


class wcolor(ITuple):
    """
    顏色定義方式:
    #00FF00 -> 0, 255, 0
    #0F0 -> #00FF00 -> 0, 255, 0
    0, 255, 0
    """
    _HEXSTR: str = '0123456789ABCDEF'

    def __init__(self, *args, **kwargs):
        """
        :param args:
            '#00FF00'
            '#0F0'
            0, 255, 0
        :param kwargs: r, g, b
        """
        self.r = 0
        self.g = 0
        self.b = 0

        if args:
            s, *_ = args
            if isinstance(s, str):
                if not s.startswith('#'):
                    raise ValueError('args is str and must startwith "#"')
                elif len(s) != 4 and len(s) != 7:
                    raise ValueError('args is str and must #fff or #ffffff')
                elif len(s) == 4:
                    s = s.upper()[1:]
                    nlist = [self._HEXSTR.index(s1) for s1 in s]
                    self.r, self.g, self.b = [16 * n + n for n in nlist]
                elif len(s) == 7:
                    s = s.upper()[1:]
                    nlist = [self._HEXSTR.index(s1) for s1 in s]
                    self.r, self.g, self.b = [
                        nlist[2 * i] * 16 + nlist[2 * i + 1] for i in range(3)]
            elif len(args) != 3:
                raise ValueError('len of args must 3')
            else:
                for i in args:
                    if not isinstance(i, int):
                        raise ValueError('args must [int, int, int]')
                self.r, self.g, self.b = args
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

        if self.r < 0 or self.g < 0 or self.b < 0:
            raise ValueError('r/g/b must >= 0')
        elif self.r > 255 or self.g > 255 or self.b > 255:
            raise ValueError('r/g/b must <= 255')

    def similar(self, *args, diff=0) -> bool:
        t: tuple
        if len(args) == 1:
            other = args[0]
            if isinstance(other, ITuple):
                t = other.totup()
            else:
                wc = wcolor(other)
                t = wc.totup()
        elif len(args) == 3:
            t = args
        else:
            raise ValueError('{} type is not support'.format(args))

        for i, v in enumerate(self.totup()):
            if abs(t[i] - v) > diff:
                return False
        return True

    def totup(self):
        return (self.r, self.g, self.b)

    def __add__(self, other):
        if isinstance(other, int):
            return wcolor(*(i + other for i in self.totup()))
        elif isinstance(other, tuple):
            if len(other) == 3:
                o = other
            else:
                raise ValueError('len of {} must 3'.format(other))
            a = []
            for i, v in enumerate(self.totup()):
                a.append(o[i] + v)
            return wcolor(*a)
        else:
            raise ValueError('{} type not support'.format(type(other)))

    def __sub__(self, other):
        if isinstance(other, collections.Iterable):
            return self.__add__(tuple(-1 * i for i in other))
        else:
            return self.__add__(-1 * other)

    def __eq__(self, other):
        if isinstance(other, str):
            try:
                o = wcolor(other)
                return self == o
            except:
                return False
        else:
            return super().__eq__(other)

    def __str__(self):
        return '{}'.format(self.totup())


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

    def grab(self, bbox=None):
        '''
        take a screenshot of window
        '''
        self.focus()

        if bbox:
            rect = bbox
        else:
            rect = self.rect

        self.image = ImageGrab.grab(rect)
        return self.image

    def get_pixel_color(self, *args, image=None) -> wcolor:
        p: wpos = None
        if len(args) == 1 and isinstance(args[0], wpos):
            p = args[0]
        else:
            p = wpos(*args)

        if image:
            im = image
        else:
            if not self.image:
                self.grab()
            im = self.image

        return wcolor(*im.getpixel(p.totup()))

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

    def mouse_move(self, from_rloc: tuple, to_rloc: tuple, rate: int = 1000):
        src_rpos: tuple[int, int] = from_rloc
        dest_rpos: tuple[int, int] = to_rloc
        if not src_rpos:
            src_rpos = self.m.position()

        src_pos = self.abspos(*src_rpos)
        dest_pos = self.abspos(*dest_rpos)

        npoints = int(
            np.sqrt((dest_pos[0]-src_pos[0])**2 + (dest_pos[1]-src_pos[1])**2) / (rate/1000))
        for i in range(npoints):
            x = int(src_pos[0] + ((dest_pos[0]-src_pos[0])/npoints)*i)
            y = int(src_pos[1] + ((dest_pos[1]-src_pos[1])/npoints)*i)
            self.m.move(x, y)
            time.sleep(0.001)

    def minimize(self):
        hwnd = self.hwnd

        if(win32gui.GetForegroundWindow() == hwnd):
            if(not win32gui.IsIconic(hwnd)):
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

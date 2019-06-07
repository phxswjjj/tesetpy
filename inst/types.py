"""定義通用類型: Position, Rectangle"""
from abc import ABCMeta, abstractmethod


class Position:
    """(x, y)，可用 Position == (x, y) 判斷"""

    def __init__(self, *args, **kwargs):
        """
        :param args: (x, y)
        :param kwargs: x, y
        """
        self._x: int = 0
        self._y: int = 0

        if args:
            if len(args) == 2:
                self._x, self._y = args
            else:
                raise ValueError('len of *args must 2')
        else:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def add(self, pos: 'Position'):
        """offset"""
        return Position(self.x + pos.x, self.y + pos.y)

    def minus(self, pos: 'Position'):
        """offset"""
        return Position(self.x - pos.x, self.y - pos.y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    @property
    def x(self):
        """x axis"""
        return self._x

    @property
    def y(self):
        """y axis"""
        return self._y


class Rectangle:
    """矩型. 使用左上、右下座標記錄，如使用其他位置則會自動轉換"""

    def __init__(self, position1, position2):
        self.pos1 = position1
        self.pos2 = position2

    @property
    def width(self):
        return abs(self.pos1.x - self.pos2.x)

    @property
    def height(self):
        return abs(self.pos1.y - self.pos2.y)

    def __str__(self):
        return '{}, {}, width={}, height={}'.format(self.pos1, self.pos2, self.width, self.height)


class ITuple(metaclass=ABCMeta):
    @abstractmethod
    def totup(self):
        pass

    def __eq__(self, other):
        if isinstance(other, ITuple):
            return self.totup() == other.totup()
        elif isinstance(other, tuple):
            return self.totup() == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

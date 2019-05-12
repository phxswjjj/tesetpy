class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, position):
        return Position(self.x + position.x, self.y + position.y)

    def minus(self, position):
        return Position(self.x - position.x, self.y - position.y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

class Rectangle:
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

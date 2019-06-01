from .win32 import wrect, wsize, wnd
from .types import Position


def test_rect():
    wr = wrect(1, 2, 3, 4)
    assert wr == (1, 4, 3, 2)

    wr = wrect(left=1, top=2, right=3, bottom=4)
    assert wr == (1, 4, 3, 2)

    wr = wrect(pos1=(1, 2), pos2=(3, 4))
    assert wr == (1, 4, 3, 2)

    wr = wrect(pos1=Position(1, 2), pos2=Position(3, 4))
    assert wr == (1, 4, 3, 2)
    assert wr != (0, 4, 3, 2)


def test_wsize():
    ws = wsize(1, 2)
    assert ws == (1, 2)

    ws = wsize(1, 2, 3, 4)
    assert ws == (2, 2)

    ws = wsize(size=(2, 2))
    assert ws == (2, 2)

    ws = wsize(width=2, height=2)
    assert ws == (2, 2)

    ws = wsize(pos1=(1, 2), pos2=(3, 4))
    assert ws == (2, 2)

    ws = wsize(pos1=Position(1, 2), pos2=Position(3, 4))
    assert ws == (2, 2)
    assert ws != (1, 2)

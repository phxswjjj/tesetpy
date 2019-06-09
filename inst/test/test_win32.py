from inst.win32 import wpos, wrect, wsize, wcolor, wnd


def test_wpos():
    wp = wpos(1, 2)
    assert wp == (1, 2)
    assert wp != (2, 1)

    wp = wpos(x=1, y=2)
    assert wp == (1, 2)
    assert wp == wpos(1, 2)

    # 比較
    assert wp != wpos(2, 1)
    assert wpos(1, 2) == wpos(1, 2)
    assert wpos(1, 2) != wpos(2, 1)


def test_wpos_op():
    wp = wpos(1, 2)
    assert wp + wp == (2, 4)
    assert wp + (-1, -1) == (0, 1)
    assert wp - (1, 1) == (0, 1)
    assert wp - (0, -1) == (1, 3)
    assert wp + 1 == (2, 3)
    assert wp - 1 == (0, 1)


def test_rect():
    wr = wrect(1, 2, 3, 4)
    assert wr == (1, 4, 3, 2)

    wr = wrect(left=1, top=2, right=3, bottom=4)
    assert wr == (1, 4, 3, 2)

    wr = wrect(pos1=(1, 2), pos2=(3, 4))
    assert wr == (1, 4, 3, 2)

    # 比較
    assert wr != (0, 4, 3, 2)
    assert wrect(1, 2, 3, 4) == wrect(1, 2, 3, 4)
    assert wrect(1, 2, 3, 4) == wrect(3, 4, 1, 2)
    assert wrect(1, 2, 3, 4) != wrect(0, 2, 3, 4)

def test_rect_op():
    wr = wrect(1, 2, 3, 4)  # convert to (1, 4, 3, 2)
    assert wr + 1 == (2, 5, 4, 3)
    assert wr - 1 == (0, 3, 2, 1)
    assert wr + (1, 2) == (2, 6, 4, 4)
    assert wr - (1, 2) == (0, 2, 2, 0)
    assert wr - (-1, -2) == (2, 6, 4, 4)
    assert wr + (1, 1, 2, 2) == (2, 5, 5, 4)
    assert wr - (1, 1, 2, 2) == (0, 3, 1, 0)

def test_wsize():
    # width, height
    ws = wsize(1, 2)
    assert ws == (1, 2)

    ws = wsize(size=(2, 2))
    assert ws == (2, 2)

    ws = wsize(width=2, height=2)
    assert ws == (2, 2)

    # 兩個座標
    ws = wsize((1, 2), (3, 4))
    assert ws == (2, 2)
    ws = wsize((3, 2), (1, 4))
    assert ws == (2, 2)

    ws = wsize(1, 2, 3, 4)
    assert ws == (2, 2)
    ws = wsize(3, 2, 1, 4)
    assert ws == (2, 2)

    ws = wsize(pos1=(1, 2), pos2=(3, 4))
    assert ws == (2, 2)
    ws = wsize(pos1=(3, 2), pos2=(1, 4))
    assert ws == (2, 2)

    ws = wsize(pos1=(1, 2), pos2=wpos(3, 4))
    assert ws == (2, 2)
    ws = wsize(pos1=wpos(3, 4), pos2=(1, 2))
    assert ws == (2, 2)

    # 比較
    assert ws != (1, 2)
    assert wsize(1, 2) == wsize(1, 2)
    assert wsize(1, 2) != wsize(2, 1)

def test_wsize_op():
    ws = wsize(1, 2)
    assert ws + 1 == (2, 3)
    assert ws - 1 == (0, 1)
    assert ws + (1, 1) == (2, 3)
    assert ws - (1, 1) == (0, 1)
    assert ws - wsize(1, 1) == (0, 1)

def test_color():
    wc = wcolor('#0f0')
    assert wc == (0, 255, 0)

    wc = wcolor('#00FF00')
    assert wc == (0, 255, 0)

    wc = wcolor(0, 255, 0)
    assert wc == (0, 255, 0)

    wc = wcolor(r=0, g=255, b=0)
    assert wc == (0, 255, 0)

    # 比較
    assert wc != (0, 0, 0)
    assert wcolor(1, 2, 3) == wcolor(1, 2, 3)

    wc = wcolor('#0f0')
    assert str(wc) == '(0, 255, 0)'

def test_color_op():
    wc = wcolor('#1e1')     # (17, 238, 17)
    assert wc + 1 == (18, 239, 18)
    assert wc - 1 == (16, 237, 16)
    assert wc + (1, 1, 1) == (18, 239, 18)


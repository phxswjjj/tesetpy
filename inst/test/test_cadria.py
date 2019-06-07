from inst.cadria import wnd


def test_wnd():
    w = wnd()
    w.load()
    assert w.hwnd != 0

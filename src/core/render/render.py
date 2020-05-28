import curses

STDSCR = None


def setup():
    global STDSCR
    STDSCR = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    STDSCR.keypad(True)
    return STDSCR


def tear_down():
    assert STDSCR is not None, "You need to call setup before calling tear_down"
    curses.nocbreak()

    # noinspection PyUnresolvedReferences
    STDSCR.keypad(False)
    curses.echo()
    curses.curs_set(1)
    curses.endwin()

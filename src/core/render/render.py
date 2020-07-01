"""
This is where the rendering happens.
"""

import curses
from typing import Any, Optional
from time import sleep


class CursesRenderer:
    def __init__(self) -> None:
        self.stdscr: Optional[curses._CursesWindow] = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

    @property
    def max_x(self):
        _, x = self.stdscr.getmaxyx()
        return x

    @property
    def max_y(self):
        y, _ = self.stdscr.getmaxyx()
        return y

    # def setup(self) -> Any:
    #     self.stdscr = curses.initscr()
    #     curses.noecho()
    #     curses.cbreak()
    #     curses.curs_set(0)
    #     self.stdscr.keypad(True)
    #     return self.stdscr
    #
    def tear_down(self) -> None:
        assert self.stdscr is not None, "You need to call setup before calling tear_down"
        curses.nocbreak()

        # noinspection PyUnresolvedReferences
        self.stdscr.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def render(self):
        # render
        self.clear_screen()

        self.addinto(0, 0, "Mind-Control based roguelike.")
        self.addinto(0, 1, "Window size: ({}, {}).".format(self.max_x, self.max_y))

        self.stdscr.box()

        # stdscr.refresh()
        self.refresh()
        curses.beep()

    def refresh(self):
        self.stdscr.refresh()

    def wait_keypress(self):
        self.stdscr.getkey()

    def clear_screen(self):
        self.stdscr.clear()

    def addtext(self, x, y, text):
        self._move_cursoryx(y, x)
        self.stdscr.addstr(text)

    def addinto(self, x, y, text):
        assert x < self.max_x
        assert y < self.max_y
        self._move_cursoryx(y+1, x+1)
        self.stdscr.addstr(text)

    def _move_cursoryx(self, y, x):
        self.stdscr.move(y, x)

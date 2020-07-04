"""
This is where the rendering happens.
"""

import curses


class CursesRenderer:
    """
    A renderer using the curses library
    """

    def __init__(self) -> None:
        self.stdscr: curses._CursesWindow = curses.initscr()  # pylint: disable=E1101

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(True)

        self.stdscr.box()

    @property
    def max_x(self) -> int:
        """
        return the maximum x size of the screen
        """
        _, max_x = self.stdscr.getmaxyx()
        return max_x

    @property
    def max_y(self) -> int:
        """
        returns the maximum y size of the screen
        """
        max_y, _ = self.stdscr.getmaxyx()
        return max_y

    def get_key(self):
        return self.stdscr.getkey()

    # def get_key_non_blocking(self):
    #     self.stdscr.nodelay(True)
    #     try:
    #         key = self.stdscr.get_wch()
    #     except:
    #         key = ""
    #     self.stdscr.nodelay(False)
    #     return key

    def wait_keypress_delay(self, delay):
        self.stdscr.timeout(round(delay * 1000)) # the delay is given in seconds, but milliseconds are expected.
        key = self.stdscr.getch()
        self.stdscr.timeout(-1)
        return key


    def tear_down(self) -> None:
        """
        Resume normal terminal state
        """
        assert (
            self.stdscr is not None
        ), "You need to call setup before calling tear_down"
        curses.nocbreak()

        # noinspection PyUnresolvedReferences
        self.stdscr.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.endwin()

    def render(self) -> None:
        """
        Render the screen
        """
        # render
        self.clear_screen()

        self.addinto(0, 0, "Press 'q' to quit.")
        self.addinto(0, 1, "Window size: ({}, {}).".format(self.max_x, self.max_y))

        self.stdscr.box()

        # stdscr.refresh()
        self.refresh()
        curses.beep()

    def refresh(self) -> None:
        """
        Refresh the screen
        """
        self.stdscr.refresh()

    def wait_keypress(self) -> None:
        """
        Wait for a key to be pressed, then return None.
        """
        self.stdscr.getkey()

    def clear_screen(self) -> None:
        """
        Clear the screen.
        """
        self.stdscr.clear()
        self.stdscr.box()

    def addtext(self, x_pos: int, y_pos: int, text: str) -> None:
        """
        Add text <text> into the main screen at position (<x_pos>, <y_pos>).
        """
        assert x_pos > -1
        assert y_pos > -1, f"y_pos: {y_pos}"
        self._move_cursoryx(y_pos, x_pos)
        self.stdscr.addstr(text)

    def addinto(self, x_pos: int, y_pos: int, text: str) -> None:
        """
        Adds text <text> into the main screen at position (<x_pos>, <y_pos>).
        The position will be modified so that the text is not drawn on
        top of the window borders.
        """
        assert x_pos < self.max_x
        assert y_pos < self.max_y, f"y_pos: {y_pos}, max: {self.max_y}"
        self._move_cursoryx(y_pos + 1, x_pos + 1)
        self.stdscr.addstr(text)

    def _move_cursoryx(self, y_pos: int, x_pos: int) -> None:
        self.stdscr.move(y_pos, x_pos)

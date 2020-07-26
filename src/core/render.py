"""
This is where the rendering happens.
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import curses
import logging
from curses import textpad
from typing import Any, Optional

logger = logging.getLogger(__name__)
# logger.level = logging.INFO  # comment out this line if you are trying to debug this


class CursesRenderer:
    """
    A renderer using the curses library
    """

    def __init__(self) -> None:
        logger.debug("Crate CursesRenderer and init curses")
        self.stdscr: Any = curses.initscr()  # pylint: disable=E1101

        self.last_key = ""

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
        self.stdscr.keypad(True)

        self.stdscr.box()

    @property
    def max_x(self) -> int:
        """
        return the maximum x size of the screen
        """
        # noinspection PyUnusedLocal
        max_x: int = 0
        _, max_x = self.stdscr.getmaxyx()

        logger.debug("Max x: %s", max_x)

        return max_x

    @property
    def max_y(self) -> int:
        """
        returns the maximum y size of the screen
        """
        # noinspection PyUnusedLocal
        max_y: int = 0
        max_y, _ = self.stdscr.getmaxyx()

        logger.debug("Max y: %s", max_y)

        return max_y

    def get_key(self) -> str:
        """
        Wait for a key to be pressed, and return a string representing it.
        """
        key: str = self.stdscr.getkey()

        key_repr = self.get_key_repr(key)
        self.last_key = key_repr

        logger.debug("Got key: %s", key)

        return key

    @staticmethod
    def get_key_repr(key: str) -> str:
        """
        Return a string representation of the given key
        """
        if key == "\n":
            key_repr = "KEY_ENTER"
        elif key == " ":
            key_repr = "KEY_SPACE"
        else:
            key_repr = key

        logger.debug("Got key representation: %s", key_repr)

        return key_repr

    def wait_keypress_delay(self, delay: float) -> int:
        """
        Wait for a key press or for the delay to pass, then return the pressed key. If no key was
        pressed, return -1.

        :param delay: For how long to wait for a key press, in seconds.
        :return: The key pressed, or -1 if no key was pressed.
        """
        self.stdscr.timeout(round(delay * 1000))  # the delay is given in seconds, but
        # milliseconds are expected.
        key: int = self.stdscr.getch()
        if key != -1:
            self.last_key = "SKIP"

            logger.debug("skipped delay")
        else:
            logger.debug("did not skip delay")

        self.stdscr.timeout(-1)

        return key

    def tear_down(self) -> None:
        """
        Resume normal terminal state
        """

        logger.info("Reverting to normal terminal state")

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

        logger.info("Rendering game")

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
        logger.debug("Refreshing screen")

        self.addinto(self.max_x - 2 - len(self.last_key), self.max_y - 2, self.last_key)
        self.stdscr.refresh()

    def wait_keypress(self) -> None:
        """
        Wait for a key to be pressed, then return None.
        """
        logger.debug("Waiting for key")

        self.stdscr.getkey()

    def clear_screen(self) -> None:
        """
        Clear the screen.
        """
        logger.debug("Clearing screen")

        self.stdscr.clear()
        self.stdscr.box()

    def addtext(
        self, x_pos: int, y_pos: int, text: str, color_pair: Optional[int] = None
    ) -> None:
        """
        Add text <text> into the main screen at position (<x_pos>, <y_pos>).
        """
        logger.debug(
            "Adding text '%s' at (%s, %s) with color %s", text, x_pos, y_pos, color_pair
        )

        if color_pair is None:
            color_pair = curses.color_pair(0)
        assert x_pos > -1
        assert y_pos > -1, f"y_pos: {y_pos}"
        self._move_cursoryx(y_pos, x_pos)
        self.stdscr.addstr(text, color_pair)

    def addinto(self, x_pos: int, y_pos: int, text: str) -> None:
        """
        Adds text <text> into the main screen at position (<x_pos>, <y_pos>).
        The position will be modified so that the text is not drawn on
        top of the window borders.
        """
        logger.debug("Adding text into screen %s at (%s, %s)", text, x_pos, y_pos)

        assert x_pos < self.max_x
        assert y_pos < self.max_y, f"y_pos: {y_pos}, max: {self.max_y}"
        self._move_cursoryx(y_pos + 1, x_pos + 1)
        self.stdscr.addstr(text)

    def _move_cursoryx(self, y_pos: int, x_pos: int) -> None:
        try:
            self.stdscr.move(y_pos, x_pos)
            logger.debug("Moved cursor to (%s, %s)", x_pos, y_pos)
        except curses.error:
            max_x = self.max_x
            max_y = self.max_y
            raise Exception(
                f"Tried to move cursor: failed: y_pos: {y_pos}, x_pos: {x_pos}, "
                f"max_x: {max_x}, max_y: {max_y}"
            )

    def move_cursorxy(self, x_pos: int, y_pos: int) -> None:
        """
        Move the cursor to the given position

        :param x_pos: x position where the cursor should be moved
        :param y_pos: y position where the cursor should be moved
        """
        self._move_cursoryx(y_pos, x_pos)

    def text_input(self, prompt: str, x_pos: int, y_pos: int, length: int) -> str:
        """
        Get some input from the user, and return it. Similar to built-in input(), but for curses

        :param prompt: A short text inviting the user to input something.
        :param x_pos: The x position where the prompt should be displayed
        :param y_pos: The y position where the prompt should be displayed
        :param length: The length of prompt. This will also limit the length of returned text.
        length - 1 characters can be returned.
        :return: The text imputed by the user, terminated by a carriage return.
        """
        logger.info(
            "Getting text input at (%s, %s) of max length %s", x_pos, y_pos, length
        )
        curses.curs_set(2)

        self.addtext(x_pos, y_pos, prompt)
        self.refresh()

        correct_x_pos = x_pos + len(prompt)

        win = curses.newwin(1, length, y_pos, correct_x_pos)
        win.bkgd(" ", curses.A_UNDERLINE | curses.A_BOLD)

        pad = textpad.Textbox(win, insert_mode=True)
        text = pad.edit()
        text = text.strip()

        win.bkgd(" ", curses.A_NORMAL)
        win.refresh()
        win = curses.newwin(1, len(text) + 1, y_pos, correct_x_pos)
        win.addstr(0, 0, text, curses.A_BOLD)
        win.refresh()

        curses.curs_set(0)
        logger.info("The user entered: %s", text)
        return text

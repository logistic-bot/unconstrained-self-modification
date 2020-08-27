"""
This file implements the FullScreenScene class, which contains convenience methods for all Scenes.
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
from abc import ABC
from typing import Optional, Any, List

from src.core.render import CursesRenderer
from src.core.state.game_state import GameState
from src.core.state.save_manager import SaveManager

logger = logging.getLogger(__name__)


class Scene:
    """
    The base class for all Scenes, contains convenience methods.
    """

    def __init__(self, renderer: CursesRenderer, state: GameState) -> None:
        self.state = state
        self.renderer = renderer

        logger.debug("Created new Scene")

    def start(self) -> Any:
        """
        Run the scene. Should be overridden by subclasses. Should return the next scene. If None
        is returned, exit the game.
        """

        logger.error("Tried to call start() on a Scene class and not a subclass!")

        raise NotImplementedError(
            "This class is not to be used directly, please create a "
            "subclass and override the start method."
        )

    def sleep_key(self, delay: float) -> bool:
        """
        Wait until a key is pressed, or the delay is exceeded.

        For more documentation, see CursesRenderer.wait_keypress_delay()

        :param delay: How many seconds to wait for a key press
        """

        logger.debug("sleeping for %s seconds", delay)

        if delay == 0:
            return False

        key = self.renderer.wait_keypress_delay(delay)

        if key != -1:
            logger.debug("Sleep interrupted!")
            return False
        return True

    def get_key(self) -> str:
        """
        Wait for a key to be pressed, and return a string representing it.
        :return: The pressed key
        """
        logger.debug("Getting key...")
        return self.renderer.get_key()

    def refresh(self) -> None:
        """
        Refresh the screen, making sure that all modified characters are displayed correctly.
        :return:
        """
        logger.debug("Refreshing screen")
        self.renderer.refresh()

    def clear(self) -> None:
        """
        Clear the screen, and redraw the borders.
        """
        logger.debug("Clearing screen")
        self.renderer.clear_screen()

    def addinto(self, x_pos: int, y_pos: int, text: str, color_pair: int = 0) -> None:
        """
        Add a text into the screen, and refresh it.

        See CursesRenderer.addtext() for details.

        :return: None
        """
        self.renderer.addtext(x_pos, y_pos, text, color_pair)
        self.refresh()

    def prompt(self, x_pos: int, y_pos: int, prompt: str = "", length: int = 30) -> str:
        """
        Get some input from the user. for more information, see CursesRenderer.text_input()
        """
        logger.debug(
            "Getting input from user at (%s, %s), with prompt %s and max length %s",
            x_pos,
            y_pos,
            prompt,
            length,
        )

        text = self.renderer.text_input(prompt, x_pos, y_pos, length)

        logger.debug("Got text: %s", text)
        return text

    @staticmethod
    def get_saves() -> List[GameState]:
        """
        Return a name-sorted list of all saved games.
        """
        save_manager = SaveManager()
        saves = save_manager.saves
        saves.sort(key=lambda x: x.data["name"].lower())
        return saves


class FullScreenScene(Scene, ABC):
    """
    The base class for all full-screen Scenes, contains convenience methods.
    """

    # TODO: Add logging for this class

    def _addinto_centred_paged(
        self, y_pos: int, text: str, delay: float, pager_delay: float, color_pair: int
    ) -> bool:
        logger.info(
            "_addinto_centred_paged: y_pos: '%s' text: '%s' delay: '%s' pager_delay: '%s' color_pair: '%s'",
            y_pos,
            text,
            delay,
            pager_delay,
            color_pair,
        )
        all_lines = text.splitlines()
        max_lines = self.renderer.max_y - 2

        # We will first show as many lines as we can, then recurse with the remaining lines
        next_lines = "\n".join(all_lines[:max_lines])
        max_lines_with_buffer = max_lines - 5
        remaining_lines = "\n".join(all_lines[max_lines_with_buffer:])

        # If the text was skipped, skip will be True
        skip = self.addinto_centred(y_pos, next_lines, delay, pager_delay, color_pair)

        # We wait for an additional delay between each page. skip_all will be True if the
        # delay is skipped, in that case we don't display the next pages.
        self.sleep_key(pager_delay)
        self.clear()  # clear the screen for the next page

        if (
            skip
        ):  # If the text animation was skipped, skip the text animation for the next
            # pages
            # This works because the delay is reused when recursing
            delay = 0

        self.addinto_centred(y_pos, remaining_lines, delay, pager_delay, color_pair)  #
        # recurse for
        # the
        # remaining lines

        self.sleep_key(pager_delay)

        return skip  # if anything was skipped, return True

    def addinto_centred(  # pylint: disable=R0913
        self,
        y_pos: int,
        text: str,
        delay: float = 0,
        pager_delay: float = 2,
        color_pair: Optional[int] = None,
    ) -> bool:
        """
        Add a text into, centered vertically, with optional delay between lines.

        If the terminal is not tall enough, the text will be paged. In that case, the parameter
        pager_delay is used to delay each page.

        :param color_pair: The color pair to use
        :param y_pos: The y position where the text should be displayed
        :param text: The text to be displayed
        :param delay: Delay between each line
        :param pager_delay: Delay between each page
        :return: True if the text was skipped, False otherwise
        """
        logger.info(
            "addinto_centred: y_pos: '%s' text: '%s' delay: '%s' pager_delay: '%s' color_pair: '%s'",
            y_pos,
            text,
            delay,
            pager_delay,
            color_pair,
        )

        # We can not set color pairs before curses is initialized, so we have to do it here.
        if color_pair is None:
            color_pair = curses.color_pair(0)

        line_count = len(text.splitlines())
        max_lines = self.renderer.max_y - 2

        if y_pos < 1:
            # Fix potential issues with incorrect y_pos

            # When this is called from addinto_all_centred, and the text is too long, y_pos will
            # be negative; this fixes that.
            y_pos = 1

        # If the text is too long for the terminal, it needs to be paged.
        if line_count > max_lines:  # -2 for the borders
            self._addinto_centred_paged(y_pos, text, delay, pager_delay, color_pair)

        else:
            # To add a delay between each line, we loop over each line
            for idx, line in enumerate(text.splitlines()):
                delay = self._add_line_centred(color_pair, delay, idx, line, y_pos)

        return delay == 0  # If something was skipped, return True

    def _add_line_centred(
        self, color_pair: int, delay: float, idx: int, line: str, y_pos: int
    ) -> float:
        logger.info(
            "_add_line_centred: color_pair: '%s' delay: '%s' idx: '%s' line: '%s' y_pos: '%s'",
            color_pair,
            delay,
            idx,
            line,
            y_pos,
        )

        middle_of_screen = self.renderer.max_x / 2
        middle_of_text = len(line) / 2
        # we need to round this to avoid passing a float to self.renderer.add_text
        x_pos = round(middle_of_screen - middle_of_text)
        correct_y_pos = y_pos + idx  # Shift each new line downwards
        self.renderer.addtext(x_pos, correct_y_pos, line, color_pair)
        self.refresh()  # to view each line being added, we need to refresh the screen
        if line != "":
            full_delay = self.sleep_key(
                delay
            )  # full delay is True if the delay was not skipped
            if (
                not full_delay
            ):  # if the delay was skipped make the delay 0 and do not wait for
                # following lines
                delay = 0
        return delay

    def addinto_all_centred(
        self, text: str, delay: float = 0, pager_delay: float = 2, color_pair: int = 0
    ) -> bool:
        """
        Adds a text into the canvas, completely centred.

        For more documentation, see FullScreenScene.addinto_centred()

        :param color_pair: The color pair to use
        :param text: The text to be displayed
        :param delay: How many seconds to wait between each line
        :param pager_delay: How many seconds to wait between each page.
        """
        logger.info(
            "addinto_all_centred: text: '%s' delay: '%s' pager_delay: '%s' color_pair: '%s'",
            text,
            delay,
            pager_delay,
            color_pair,
        )

        line_count = len(text.splitlines())
        return self.addinto_centred(
            round(self.renderer.max_y / 2) - round(line_count / 2),
            text,
            delay,
            pager_delay,
            color_pair,
        )

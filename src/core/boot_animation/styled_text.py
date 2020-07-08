# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#  Copyright (C) © 2020 Khaïs COLIN <logistic-bot@protonmail.com>
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
from typing import Optional

from src.core.render import CursesRenderer


class StyledText:
    """
    This class is used to draw styled text. It abstracts away curses attributes system.

    :param renderer: A renderer instance to show the styled text
    :param text: The text to be styled
    :param color: A curses color pair number

    :param inverted: If the text colors should be inverted
    :param blinking: If the text should be blinking
    :param bold: If the text should be bold
    :param italic: If the text should be italic
    """

    def __init__(
        self,
        renderer: Optional[CursesRenderer],
        text: Optional[str] = None,
        color: int = 0,
        inverted: bool = False,
        blinking: bool = False,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        effects = curses.A_NORMAL
        if inverted:
            effects = effects | curses.A_REVERSE
        if blinking:
            effects = effects | curses.A_BLINK
        if bold:
            effects = effects | curses.A_BOLD
        if italic:
            effects = effects | curses.A_ITALIC

        self.font = curses.color_pair(color) | effects
        self.text = text
        self.renderer = renderer

    @property
    def draw(self) -> bool:
        """
        Returns true if there is something to draw
        """
        if self.text is None:
            return False
        return True

    def show(self, x_pos: int, y_pos: int) -> None:
        """
        Show the styled text at the given position
        :return: None
        """
        assert self.renderer is not None
        if self.draw:
            assert isinstance(self.text, str)
            self.renderer.addtext(x_pos, y_pos, self.text, self.font)
        self.renderer.refresh()

"""
This file contains the StyledText class, which stores style information for a string,
abstracting away the curses problems.
"""

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

# TODO: REFACTORING BOOT_ANIMATION PLAN
# TODO: Refactor Stage.
from __future__ import annotations

import curses
from typing import Optional, Union, List

from src.core.render import CursesRenderer


class StyledText:
    """
    This class is used to draw text with colors, and different curses attributes.
    """

    def __init__(self, renderer: Optional[CursesRenderer],
                 text: Union[str, List[str], List[StyledText]], color: int = 0,
                 invert: bool = False, blink: bool = False, bold: bool = False,
                 italic: bool = False, dim=False) -> None:
        self.italic = italic
        self.bold = bold
        self.blink = blink
        self.invert = invert
        self.dim = dim

        self.renderer = renderer
        self.color = color

        self.text = text

    @property
    def effects(self) -> int:
        """
        Get the int representing the effects applied to the text.
        """
        effects = curses.A_NORMAL
        if self.invert:
            effects = effects | curses.A_REVERSE
        if self.blink:
            effects = effects | curses.A_BLINK
        if self.bold:
            effects = effects | curses.A_BOLD
        if self.italic:
            effects = effects | curses.A_ITALIC
        if self.dim:
            effects = effects | curses.A_DIM
        return effects

    @property
    def font(self) -> int:
        """
        Get the int representing the curses font associated with this text.
        """
        return curses.color_pair(self.color) | self.effects

    @property
    def method(self) -> str:
        """
        Get the way in which this text should be displayed. Used internally.
        """
        # I don't know is we need this.
        if isinstance(self.text, str):
            method = "str"
        elif isinstance(self.text, list):
            if isinstance(self.text[0], str):
                method = "List[str]"
            elif isinstance(self.text[0], StyledText):
                method = "List[StyledText]"
            else:
                raise TypeError(
                    "Argument text for StyledText needs to be of type Union[str, "
                    "List[str], List[StyledText]]."
                )
        else:
            raise TypeError(
                "Argument text for StyledText needs to be of type Union[str, "
                "List[str], List[StyledText]]."
            )
        return method

    def __len__(self) -> int:
        if self.method.startswith("List"):
            lens = [len(text) for text in self.text]
            return sum(lens)
        return len(self.text)

    def show(self, x_pos: int, y_pos: int) -> None:
        """
        Show the text at the given position.
        """
        assert self.renderer is not None

        if self.method == "str":
            assert isinstance(self.text, str)
            self.renderer.addtext(x_pos, y_pos, self.text, self.font)

        elif self.method == "List[str]":
            assert isinstance(self.text, list)

            for text in self.text:
                assert isinstance(text, str)
                self.renderer.addtext(x_pos, y_pos, text, self.font)
                x_pos += len(text)

        elif self.method == "List[StyledText]":
            assert isinstance(self.text, list)

            for text in self.text:
                assert isinstance(text, StyledText)
                text.show(x_pos, y_pos)
                x_pos += len(text)
        else:
            raise NotImplementedError(
                "Please try using one of the supported text types."
            )

        self.renderer.refresh()

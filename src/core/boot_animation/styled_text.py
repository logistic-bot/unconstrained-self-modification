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
# TODO: Rewrite StyledText so that it can take a list of StyledText as its text argument and is
#  accepted by CursesRenderer as a text.
# TODO: Refactor Stage.
from __future__ import annotations

import curses
from typing import Optional, Union, List, TypeVar

from src.core.render import CursesRenderer

CursesColorPairNumber = TypeVar("CursesColorPairNumber", bound=int)


class StyledText:
    """
    This class is used to draw text with colors, and different curses attributes.
    """

    def __init__(
        self,
        renderer: Optional[CursesRenderer],
        text: Union[str, List[str], List[StyledText]],
        color: CursesColorPairNumber,
        invert: bool = False,
        blink: bool = False,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        self.italic = italic
        self.bold = bold
        self.blink = blink
        self.invert = invert

        self.renderer = renderer
        self.color = color

        self.text = text

    @property
    def effects(self) -> int:
        effects = curses.A_NORMAL
        if self.invert:
            effects = effects | curses.A_REVERSE
        if self.blink:
            effects = effects | curses.A_BLINK
        if self.bold:
            effects = effects | curses.A_BOLD
        if self.italic:
            effects = effects | curses.A_ITALIC
        return effects

    @property
    def font(self) -> int:
        return curses.color_pair(self.color) | self.effects

    @property
    def method(self) -> str:
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
        else:
            return len(self.text)

    def show(self, x_pos: int, y_pos: int) -> None:
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


class OldStyledText:
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

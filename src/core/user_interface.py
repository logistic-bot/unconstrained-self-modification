# ------------------------------------------------------------------------------
#  This file is part of Unconstrained self-modification.
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
import logging
from typing import Optional, List

from src.core.render import CursesRenderer

logger = logging.getLogger(__name__)


class ListRenderer:
    def __init__(
        self,
        renderer: CursesRenderer,
        x_pos: int,
        y_pos: int,
        items: Optional[List[str]]=None,
        select_max_length: bool = False,
        max_length: Optional[int] = None,
        margin: int = 0,
    ) -> None:
        # TODO: if the user changes self.items, self.max_length is not correct anymore. Use @property and self._max_length

        if items is None:
            items = []

        self._max_length = max_length
        self._selected = True

        self.y_pos = y_pos
        self.x_pos = x_pos
        self.items = items
        self.renderer = renderer
        self.index = 0

        self.indent_selected = False
        self._margin = margin
        self.select_max_length = select_max_length

        logger.info("Created new ListRenderer at ({}, {})")

    def set_margin(self, value: int) -> None:
        self._margin = value

    def get_margin(self) -> int:
        return self._margin

    margin = property(get_margin, set_margin)

    # def set_select_max_length():

    def select_next(self) -> None:
        self.select(self.index + 1)

    def select_previous(self) -> None:
        self.select(self.index - 1)

    def check_input(self, key: str) -> None:
        if self.selected:
            if key == "KEY_DOWN":
                self.select_next()
            elif key == "KEY_UP":
                self.select_previous()

    def select(self, index: int) -> None:
        try:
            assert index < len(self.items)
            assert index >= 0
            self.index = index
        except AssertionError:
            logger.warning(
                "Tried to select item at index %s but item does not exist. Items: %s",
                index,
                self.items,
            )

    @property
    def selected_item(self) -> str:
        item = self.items[self.index]
        assert isinstance(item, str)
        return item

    def get_selected(self) -> bool:
        return self._selected

    def set_selected(self, value: bool) -> None:
        self._selected = value

    selected = property(get_selected, set_selected)

    def get_max_length(self) -> int:
        if self._max_length is None:
            lens = [len(item) for item in self.items]
            logger.debug("lens: '%s'", lens)
            max_length = max(lens)
        else:
            max_length = self._max_length

        logger.debug("got max_length '%s'", max_length)
        return max_length

    def set_max_length(self, value: int) -> None:
        self._max_length = value

    max_length = property(get_max_length, set_max_length)

    @property
    def actual_width(self) -> int:
        text = " " * self.max_length
        width = len(self.get_item_margins(text))
        if self.indent_selected:
            width += 1
        logger.debug("got actual_width: '%s'", width)
        return width

    def draw(self) -> None:
        # draw the list
        for index, item in enumerate(self.items):
            item = self.get_item_margins(item)

            self.renderer.addtext(self.x_pos, self.y_pos + index, " " * (len(item) + 1))
            self.renderer.addtext(self.x_pos, self.y_pos + index, item)

        self.highlight_selected()

    def get_item_margins(self, item: str) -> str:
        if self.select_max_length:
            item += " " * (self.max_length - len(item))
            logger.debug("item: '%s'", item)
            logger.debug("item len: '%s'", len(item))

        item = " " * self.margin + item + " " * self.margin
        return item

    def highlight_selected(self) -> None:
        item = self.get_item_margins(self.selected_item)

        selected_x_pos = self.x_pos
        if self.indent_selected:
            selected_x_pos += 1

        if self.selected:  # if selected
            self.renderer.addtext(
                self.x_pos, self.y_pos + self.index, " " * self.max_length
            )

            self.renderer.addtext(
                selected_x_pos,
                self.y_pos + self.index,
                item,
                curses.A_BOLD | curses.A_REVERSE,
            )
        else:  # if not selected
            self.renderer.addtext(
                self.x_pos,
                self.y_pos + self.index,
                item,
                curses.A_DIM | curses.A_REVERSE,
            )


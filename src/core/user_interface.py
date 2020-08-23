"""
Thie module contains user_interface facilities. Various class to simplify
building user interfaces.
"""

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
from typing import Optional, List, Union, cast

from src.core.render import CursesRenderer

logger = logging.getLogger(__name__)


class ListRenderer:
    """
    Allows to render a list of strings. This can also be used to select one of
    the strings from the list.
    """

    def __init__(
        self,
        renderer: CursesRenderer,
        x_pos: int,
        y_pos: int,
        items: Optional[List[str]] = None,
        select_max_length: bool = False,
        max_length: Optional[int] = None,
        margin: int = 0,
    ) -> None:
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

        logger.info(
            "Created new ListRenderer at (%s, %s) with items '%s'", x_pos, y_pos, items
        )

    def set_margin(self, value: int) -> None:
        """
        Set the margin for this ListRenderer.

        The margin dictates how many spaces should be added before and after each
        element of the list.

        Examples:
            margin = 0:
                `element 1`
                `element 2`
                `element 3`
            margin = 1:
                ` element 1 `
                ` element 2 `
                ` element 3 `
            margin = 5:
                `     element 1     `
                `     element 2     `
                `     element 3     `

        """
        self._margin = value

    def get_margin(self) -> int:
        """
        Get the current margin for this ListRenderer.

        See set_margin for a description of what a margin is.
        """
        return self._margin

    margin = property(get_margin, set_margin)

    def select_next(self) -> None:
        """
        Select the next element element in the list.
        """
        self.select(self.index + 1)

    def select_previous(self) -> None:
        """
        Select the previous element element in the list.
        """
        self.select(self.index - 1)

    def select(self, index: int) -> None:
        """
        Select a specified element in the list.

        If the given index is out of range, no change is made.

        The selected element is highlighed when the list is drawn. It can also
        be indented if ListRenderer.indent_selected is set to True.

        :param index: The index of the element to select.
        """
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

    def check_input(self, key: str) -> None:
        """
        Select the next or previous element in the list if the given key is
        KEY_DOWN or KEY_UP, respectively.

        This only has an effect when this list is selected.

        (Selected means that  the list can be acted upon. It also serves to give
        the user feedback  about whether the user can act on the list. When the
        list is selected,  the currently selected element is highlighted. When
        the list is not  selected, the currently selected element is not
        highlighted as much.)
        """
        if self.selected:
            if key == "KEY_DOWN":
                self.select_next()
            elif key == "KEY_UP":
                self.select_previous()

    @property
    def selected_item(self) -> str:
        """
        Return the currently selected item.
        """
        item = self.items[self.index]
        return item

    def get_selected_index(self) -> int:
        """
        Return the index of the currently selected item.
        """
        return self.index

    def get_selected(self) -> bool:
        """
        Return True if the list is currently selected, False otherwise.
        """
        return self._selected

    def set_selected(self, value: bool) -> None:
        """
        When given True, the list will be selected. When given False, the list
        will be unselected.
        """
        self._selected = value

    selected = property(get_selected, set_selected)

    def get_max_length(self) -> int:
        """
        Get the length of the longest element of the list, or the minimum
        highlight length.

        max_length can be in two modes: Internal or external. The mode is
        determined by whether the max_length was set or not.

        Internal mode: (default)
            Internal mode can be obtained by setting max_length to None. It is
            also the default mode, which is used if max_length is not set at
            all.

            While in internal mode, get_max_length will return the length of the
            longes element of the list.

            select_max_length will select the length of the longest element,
            automatically.

            (dev note: this is because select_max_length uses get_max_length
            internally)

        External mode:
            External mode can be obtained by setting max_length to any integer.
            If the given integer is negative, zero, or smaller that the length
            of the shortest element of the list, it will behave as if it were in
            internal mode.

            If highlight_selected and highlight_max_length are both True, then
            the ListRenderer will highlight up to max_length for element that
            are shorter than max_length and the whole element for elements that
            are longer.

            While in external mode, get_max_length will return the length set by
            set_max_length.

        (dev note: not all of the described behavior is tested, please open an
        issues if you experience any disrepancies)
        """
        if self._max_length is None:
            lens = [len(item) for item in self.items]
            logger.debug("lens: '%s'", lens)
            max_length = max(lens)
        else:
            max_length = self._max_length

        logger.debug("got max_length '%s'", max_length)
        return max_length

    def set_max_length(self, value: int) -> None:
        """
        If value is None, set the max_length mode to Internal. If value is not
        None, set the max_length mode to External and set the max_length to the
        given value.

        See get_max_length for an extended explanation of what External and
        Internal modes are.
        """
        self._max_length = value

    max_length = property(get_max_length, set_max_length)

    @property
    def actual_width(self) -> int:
        """
        Returns the width taken by drawing the list.

        It's a measure of how much vertical space will be altered when calling
        the draw() method.

        It takes into account margins, indent_selected and get_max_length.
        """
        text = " " * self.max_length
        width = len(self.get_item_margins(text))
        if self.indent_selected:
            width += 1
        logger.debug("got actual_width: '%s'", width)
        return width

    def draw(self) -> None:
        # TODO: indent_selected should be customizable, how much should it be
        # indented
        """
        Draw the list.

        Possible options:
         - margin: sets how many spaces should be inserted before and after each
           item. See also get_item_margins()

        See also highlight_selected() for option to highlight the selected item.
        """
        for index, item in enumerate(self.items):
            item = self.get_item_margins(item)

            if self.indent_selected:
                self.renderer.addtext(
                    self.x_pos, self.y_pos + index, " " * (len(item) + 1)
                )
            self.renderer.addtext(self.x_pos, self.y_pos + index, item)

        self.highlight_selected()

    def get_item_margins(self, item: str) -> str:
        """
        Given an item string, return the item with the needed margins applied.

        If select_max_length is True, we need to add a corresponding number of
        spaces to the end of the item string, to make sure that if the item is
        selected, the needed length will be highlighted. See also
        get_max_length() (Internal mode) for more details.

        See also set_margin()
        """
        if self.select_max_length:
            item += " " * (self.max_length - len(item))
            logger.debug("item: '%s'", item)
            logger.debug("item len: '%s'", len(item))

        item = " " * self.margin + str(item) + " " * self.margin
        return item

    def highlight_selected(self) -> None:
        """
        Highlight the selected item so that the user can see which item is
        selected.

        Options:
            indent_selected: If True, the selected item will be indented to the
                right by one character.
            selected: If the list is selected, the selected item will be
                highlighted brightly. If not, it will be highlighted greyly.
        """
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


class TreeListRenderer:
    """
    Allows to show two or more ListRenderer one after the other, with Automatic
    navigation between the lists.

    The lists can only be shown horizontally, with list 0 being on the left.

    The lists are completely independent of each other, so dynamically changing
    one list depending on which element is selected in another is not supported
    by this class. It can however be done manually, and this functionallity is
    planned.

    Note: whenever we talk about the 'next' or 'previous' ListRenderer, we talk
    about the ListRenderer directly to the right and left of the currently
    selected one, respectively.

    Layout: (the number indicates the index of the list)
    +-----+ +-----+ +-----+
    |     | |     | |     |
    |  0  | |  1  | |  2  |
    |     | |     | |     |
    +-----+ +-----+ +-----+
    """

    # TODO: Add a way to represent file systems with nested lists. This onl
    # allows for a defined set of actions wich are independent of the selected
    # element.
    def __init__(
        self,
        renderer: CursesRenderer,
        x_pos: int,
        y_pos: int,
        items: Union[List[List[str]], List[ListRenderer]],
    ):
        self.renderer = renderer
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.selected_list = 0
        self.margin = 1

        try:
            if isinstance(items[0], ListRenderer):
                logger.debug("Creating TreeListRenderer with List[ListRenderer]")
                passed_items = items
            elif isinstance(items[0], str):
                logger.debug("Creating TreeListRenderer with List[List[str]]")
                passed_items = self.convert_list_str_to_listrenderer(
                    renderer, cast(List[List[str]], items)
                )
            else:
                logger.warning(
                    "Unexceped type %s. Assuming List[List[str]].", type(items)
                )
                passed_items = self.convert_list_str_to_listrenderer(
                    renderer, cast(List[List[str]], items)
                )
        except IndexError:
            logger.warning(
                "Could not determine type of items. Type: %s. Assuming List[ListRenderer].",
                type(items),
            )
            passed_items = items

        self.items: List[ListRenderer] = cast(List[ListRenderer], passed_items)
        self.set_items_position()
        self.select_list(0)

    def convert_list_str_to_listrenderer(
        self, renderer: CursesRenderer, items: List[List[str]]
    ) -> List[ListRenderer]:
        """
        Convert a list of lists of strings into a corresponding list of
        ListRenderers. Used internally.
        """
        passed_items = []
        for item in items:
            list_renderer = ListRenderer(renderer, 0, 0, item)
            passed_items.append(list_renderer)

        return passed_items

    def draw(self) -> None:
        """
        Draw the TreeListRenderer.

        (draws each of the ListRenderers in sequence.)
        """
        for i in self.items:
            i.draw()

    def check_input(self, key: str) -> None:
        """
        Check if the given key is one of the handled keys, and execute the
        appropriate action.

        Handled keys include all the keys handled by ListRenderers, since the
        key is first handled by each of the ListRenderers. (at the time of
        writing, the ListRenderers can handle KEY_UP and KEY_DOWN to select the
        next and previous item in the list if the list is selected)

        KEY_RIGHT select the ListRenderer to the right of the current one, and
        KEY_LEFT select the ListRenderer to the left of the current one
        """
        for item in self.items:
            item.check_input(key)

        if key == "KEY_RIGHT":
            self.select_next_list()
        elif key == "KEY_LEFT":
            self.select_previous_list()

    def select_next_list(self) -> None:
        """
        Select the ListRenderer to the right of the current one.
        """
        self.select_list(self.selected_list + 1)

    def select_previous_list(self) -> None:
        """
        Select the ListRenderer to the left of the current one.
        """
        self.select_list(self.selected_list - 1)

    def select_list(self, index: int) -> None:
        """
        Select the ListRenderer at the given index. See the documentation for
        the whole class to understand how indexes work.

        If the index is out of range, nothing happens.

        This method will alos ensure that only one ListRenderer is currently
        selected.
        """
        if index < 0 or index >= len(self.items):
            return

        self.selected_list = index
        for list_index, item in enumerate(self.items):
            if list_index == index:
                item.selected = True
            else:
                item.selected = False

    def set_items_position(self) -> None:
        """
        Automatically adjust the positionning of the ListRenderers so that they
        conform to the layout described in the documentation for the whole
        class.

        This is called at initialization, and will need to be called manually if
        one of the ListRenderer's actual_width chages.
        """
        sum_now = self.x_pos
        for item in self.items:
            item.x_pos = sum_now
            item.y_pos = self.y_pos
            sum_now += item.actual_width + self.margin

    def get_list_item(self, index: int) -> Optional[ListRenderer]:
        """
        Return the ListRenderer at the given index. If the index is out of
        range, returns None.
        """
        if index < 0 or index >= len(self.items):
            return None
        return self.items[index]

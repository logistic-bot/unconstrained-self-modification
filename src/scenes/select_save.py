"""
This files contains the SelectSave scene, which allows the user to select a save that will then
be loaded.
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
import curses
import logging
from typing import Optional

from src.core.render import CursesRenderer
from src.core.scene import FullScreenScene, Scene
from src.core.state.game_state import GameState
from src.core.user_interface import ListRenderer, TreeListRenderer

logger = logging.getLogger(__name__)

MARGIN = 1
MAX_LENGTH = 30 - MARGIN * 2

TREE_Y_POS = 3
TREE_X_POS = 1

INFO_Y_POS = 3

SAVE_LIST_TITLE = " " + "Save files" + " "
ACTION_LIST_TITLE = " " + "Actions" + " "

TITLE_Y_POS = 1


class SelectSave(FullScreenScene):
    """
    Ask the user to select a save, then load it.
    """

    def __init__(self, renderer: CursesRenderer, state: GameState) -> None:
        super().__init__(renderer, state)

    def start(self) -> Optional[Scene]:
        """
        See above
        """

        logger.info("Starting Scene: SelectSave")

        save_list = self.create_save_list()
        action_list = self.create_action_list()

        SEPARATOR_1_POS = save_list.actual_width + 1
        SEPARATOR_2_POS = action_list.actual_width + save_list.actual_width + 2

        PROPERTIES_X_POS = SEPARATOR_2_POS + MARGIN + 1

        save_tree_list = TreeListRenderer(
            self.renderer, TREE_X_POS, TREE_Y_POS, [save_list, action_list]
        )

        def show_extra_info(save_list):
            try:
                save = self.get_saves()[save_list.index]
            except IndexError:
                pass
            else:
                infos = [
                    "Username: '{d[user][username]}'",
                    "Password: '{d[user][password]}'",
                ]

                for index, info in enumerate(infos):
                    self.addinto(
                        PROPERTIES_X_POS, INFO_Y_POS + index, info.format(d=save.data)
                    )
                    self.sleep_key(0.02)

        key = ""
        while key != "q":
            self.clear()

            # draw
            save_tree_list.draw()

            # separator
            self.show_separator(SEPARATOR_1_POS)
            self.show_separator(SEPARATOR_2_POS)

            # title
            if save_list.selected:
                save_title_color = curses.A_BOLD | curses.A_REVERSE
                action_title_color = None
            elif action_list.selected:
                save_title_color = None
                action_title_color = curses.A_BOLD | curses.A_REVERSE
            else:
                save_title_color = None
                action_title_color = None

            self.draw_centred(
                SAVE_LIST_TITLE,
                TREE_X_POS,
                SEPARATOR_1_POS,
                TITLE_Y_POS,
                save_title_color,
            )
            self.draw_centred(
                ACTION_LIST_TITLE,
                SEPARATOR_1_POS,
                SEPARATOR_2_POS,
                TITLE_Y_POS,
                action_title_color,
            )

            self.addinto(
                PROPERTIES_X_POS,
                TITLE_Y_POS,
                " Properties ",
                curses.A_DIM | curses.A_REVERSE,
            )

            show_extra_info(save_list)

            # key
            key = self.get_key()
            save_tree_list.check_input(key)

            if key == "\n":
                index = action_list.index
                if index == 0:
                    self.addinto_all_centred("LOADING...")
                elif index == 1:
                    self.addinto_all_centred("RENAMING...")
                elif index == 2:
                    self.addinto_all_centred("DELETING...")
                elif index == 3:
                    self.addinto_all_centred("CREATING...")
                else:
                    self.addinto_all_centred("IMPOSSIBLE...")
                self.sleep_key(5000)

    def create_save_list(self):
        save_list = ListRenderer(
            self.renderer, 0, 0, self.get_save_names(), True, MAX_LENGTH, MARGIN,
        )
        return save_list

    def create_action_list(self):
        action_list = ListRenderer(
            self.renderer,
            0,
            0,
            ["Load save", "Rename save", "Delete save", "Create new save"],
            True,
            MAX_LENGTH,
            MARGIN,
        )
        return action_list

    def draw_centred(self, text, left, right, y_pos, color_pair=None):
        logger.debug(
            "Drawing centred text '%s' with left %s right %s y_pos %s.",
            text,
            left,
            right,
            y_pos,
        )

        x_pos = left + round((right - left) / 2) - round(len(text) / 2)

        logger.debug("Drawing centred text '%s' at (%s, %s)", text, x_pos, y_pos)
        self.addinto(x_pos, y_pos, text, color_pair)

    def get_save_names(self):
        names = []
        for save in self.get_saves():
            names.append(save.data["name"])
        return names

    def show_separator(self, x_pos: int) -> None:
        """
        Show a separator at the given x_pos
        :param x_pos: the x_pos of the separator
        """
        self.renderer.stdscr.vline(1, x_pos, curses.ACS_VLINE, self.renderer.max_y - 2)

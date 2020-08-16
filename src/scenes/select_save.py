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
from time import sleep
from typing import Optional

from src import GAME_ROOT_DIR
from src.core.render import CursesRenderer
from src.core.scene import FullScreenScene, Scene
from src.core.state.game_state import GameState
from src.core.state.save_manager import SaveManager
from src.core.user_interface import ListRenderer, TreeListRenderer
from src.scenes.corrupted_login_new_save import CorruptedLoginNewSave
from src.scenes.start_computer import StartComputer

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

        self.last_selected_save_index = 0

        logger.info("Starting Scene: SelectSave")

        save_list = self.create_save_list()
        action_list = self.create_action_list()

        SEPARATOR_1_POS = save_list.actual_width + 1
        SEPARATOR_2_POS = action_list.actual_width + save_list.actual_width + 2

        PROPERTIES_X_POS = SEPARATOR_2_POS + MARGIN + 1

        treelist = TreeListRenderer(
            self.renderer, TREE_X_POS, TREE_Y_POS, [save_list, action_list]
        )

        ACTION_LIST_X_POS = TREE_X_POS + (MARGIN * 2) + MAX_LENGTH

        def show_info(save_list):
            if save_list.index == self.last_selected_save_index:
                delay = 0
            else:
                self.last_selected_save_index = save_list.index
                delay = 0.02

            try:
                save = self.get_saves()[save_list.index]
            except IndexError:
                pass
            else:
                infos = [
                    "Username: '{d[user][username]}'",
                    "Password: '{d[user][password]}'",
                    "Note: {d[note]}",
                ]

                for index, info in enumerate(infos):
                    try:
                        self.addinto(
                            PROPERTIES_X_POS, INFO_Y_POS + index, info.format(d=save.data)
                        )
                    except KeyError:
                        pass
                    else:
                        sleep(delay)

                computer_brand = "none"
                try:
                    logger.debug("Trying to get computer brand info from save file")
                    computer_brand = save.data["progress"]["computer-brand"]
                except KeyError:
                    logger.warning("Failed to get computer brand info from save file")

                computer_brand_path = GAME_ROOT_DIR / "assets" / "brand_logo" / computer_brand

                logger.debug("Trying to find asset at '%s'", computer_brand_path)
                try:
                    with computer_brand_path.open("r") as file:
                        computer_brand_logo = file.read()
                except FileNotFoundError:
                    computer_brand_logo = "WARNING: Asset missing. Try updating your game."

                lines = computer_brand_logo.splitlines()
                max_line_length = max([len(line) for line in lines])
                assert max_line_length < MAX_LENGTH, (
                    "There is an error with the logo file, the lines are too "
                    "long to be displayed."
                )
                x_pos = ACTION_LIST_X_POS + round(MAX_LENGTH / 2) - round(max_line_length / 2)
                y_pos = self.renderer.max_y - len(lines) - 1 # minus one for the border
                for index, line in enumerate(lines):
                    self.addinto(x_pos, y_pos + index, line)
                    sleep(delay)

        def update_save_list_names():
            save_list = self.create_save_list()
            save_list.selected = False
            treelist.items[0] = save_list
            treelist.set_items_position()

        def show_help(save_list, action_list):
            selected_save = self.get_saves()[save_list.index]
            helps = [
                "ENTER: Load save '{}'",
                "ENTER: Rename save '{}'",
                "ENTER: Delete save '{}'",
                "ENTER: Create new save",
            ]
            name = selected_save.data["name"]
            help_text = helps[action_list.index]
            help_text = help_text.format(name)
            self.renderer.add_down_bar_text(help_text, 0, curses.A_REVERSE)

        key = ""
        while key != "q":
            self.clear()

            # draw
            treelist.draw()

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

            show_help(save_list, action_list)
            show_info(save_list) # this should be last, because of the delay.

            # key
            key = self.get_key()
            treelist.check_input(key)

            if key == "\n":
                index = action_list.index
                if index == 0:  # Load game
                    self.addinto_all_centred("LOADING...")
                    self.state = self.get_saves()[save_list.index]
                    self.clear()
                    self.addinto_all_centred("Done.")
                    return StartComputer(self.renderer, self.state)
                elif index == 1:  # Rename
                    selected_state = self.get_saves()[save_list.index]
                    name = selected_state.data["name"]

                    # prompt for name
                    prompt_text = "New name for save '{}': ".format(name)
                    new_name = self.prompt(
                        round(self.renderer.max_x / 2)
                        - 15
                        - round(len(prompt_text) / 2),
                        round(self.renderer.max_y / 2),
                        prompt_text,
                    )

                    # actual renameing
                    save_manager = SaveManager()
                    save_manager.rename(selected_state, new_name)

                    # update save_list names
                    update_save_list_names()
                elif index == 2:  # Delete
                    selected_state = self.get_saves()[save_list.index]
                    name = selected_state.data["name"]

                    confirmation_prompt = " Are you sure you want to delete the save '{}'? ".format(
                        name
                    )

                    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

                    self.renderer.add_down_bar_text(
                        confirmation_prompt,
                        color_pair=curses.A_REVERSE
                        | curses.color_pair(1)
                        | curses.A_BOLD,
                    )
                    self.renderer.add_down_bar_text(
                        " [y/n] ",
                        2,
                        color_pair=curses.A_REVERSE | curses.color_pair(1),
                    )

                    key = ""
                    while key not in ("y", "n"):
                        key = self.get_key().lower()
                        if key not in ("y", "n"):
                            self.renderer.add_down_bar_text(
                                " Please press 'y' or 'n' ",
                                2,
                                color_pair=curses.A_REVERSE
                                | curses.A_BLINK
                                | curses.color_pair(1),
                            )
                        self.renderer.add_down_bar_text(
                            confirmation_prompt,
                            color_pair=curses.A_REVERSE | curses.color_pair(1),
                        )

                    if key == "y":
                        self.addinto_all_centred("Deleting save {}...".format(name))
                        SaveManager().delete(selected_state)

                    # update save_list names
                    update_save_list_names()
                elif index == 3:  # Create new
                    return CorruptedLoginNewSave(self.renderer, self.state)
                else:  # This should not be possible
                    self.addinto_all_centred("IMPOSSIBLE...")

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

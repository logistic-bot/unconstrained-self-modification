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

from src.core.scene import FullScreenScene, Scene
from src.core.state.save_manager import SaveManager
from src.scenes.start_computer import StartComputer

logger = logging.getLogger(__name__)


class SelectSave(FullScreenScene):
    """
    Ask the user to select a save, then load it.
    """

    def start(self) -> Optional[Scene]:
        """
        See above
        """

        logger.info("Starting Scene: SelectSave")
        title = " Save files "

        save_manager = SaveManager()
        saves = save_manager.saves

        # get the save with the longest name
        # TODO: truncate names too long
        longest_name = len(title)
        for save in saves:
            name = save.data["name"]
            if len(name) > longest_name:
                longest_name = len(name)

        selected_index = 0
        selected_option = 1
        save_start_y_pos = 3
        save_x_pos = 2
        key = ""
        current = saves[0]
        save_list_selected = True
        while key != "\n":
            self.clear()

            save_name_x_pos = longest_name + 3
            option_x_pos = save_name_x_pos + 2

            # show separator
            self.renderer.stdscr.vline(
                1, save_name_x_pos, curses.ACS_VLINE, self.renderer.max_y - 2
            )

            # show title
            title_start_x = round(save_name_x_pos / 2) - round(len(title) / 2)
            self.addinto(title_start_x, 1, title, curses.A_DIM | curses.A_REVERSE)

            # show the list
            for save_index, save in enumerate(saves):
                name = save.data["name"]
                self.addinto(save_x_pos, save_start_y_pos + save_index, name)

            # highlight current
            current = saves[selected_index]
            name = current.data["name"]
            y_pos_selected = save_start_y_pos + selected_index
            selected_name = " " + name.ljust(longest_name + 1, " ")
            self.addinto(
                save_x_pos - 1,
                y_pos_selected,
                selected_name,
                curses.A_BOLD | curses.A_REVERSE,
            )

            # show options
            self.addinto(option_x_pos, 1, " Actions ", curses.A_DIM | curses.A_REVERSE)

            self.addinto(option_x_pos, 3, "Load selected")
            self.addinto(option_x_pos, 4, "Rename selected")
            self.addinto(option_x_pos, 5, "Delete selected")

            self.addinto(option_x_pos, 7, "Create new")

            # show help
            help_text = ""
            if save_list_selected:
                help_text = "ENTER: load save '{}' ({})".format(
                    name, current.data["user"]["username"]
                )
            self.renderer.add_down_bar_text(help_text, 0, curses.A_REVERSE)

            # handle key
            key = self.get_key()
            # select pane
            if key == "KEY_RIGHT":
                save_list_selected = False
            elif key == "KEY_LEFT":
                save_list_selected = True
            elif key.lower() == "q":
                return None  # exit the game

            if save_list_selected:
                if key == "KEY_DOWN":
                    if selected_index < len(saves) - 1:
                        selected_index += 1
                elif key == "KEY_UP":
                    if selected_index > 0:
                        selected_index -= 1
                else:
                    logger.warning("Unhandled key '%s'", key)
            else:
                # TODO: rename save
                # TODO: create new save
                # TODO: Load save
                # TODO: delete save
                logger.warning("Unhandled key '%s'", key)

            logger.info("Selected save: '%s'", name)

        self.addinto_centred(20, "Loading '{}'...".format(current.data["name"]))

        self.state = current

        self.clear()
        self.addinto_all_centred("Done.")

        return StartComputer(self.renderer, self.state)

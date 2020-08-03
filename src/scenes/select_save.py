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
from src.core.state.save_manager import SaveManager
from src.scenes.corrupted_login_new_save import CorruptedLoginNewSave
from src.scenes.start_computer import StartComputer

logger = logging.getLogger(__name__)


class SelectSave(FullScreenScene):
    """
    Ask the user to select a save, then load it.
    """

    def __init__(
        self,
        renderer: CursesRenderer,
        state: GameState,
        selected_index: int = 0,
        selected_option: int = 1,
        save_list_selected: bool = True,
    ) -> None:
        super().__init__(renderer, state)
        self.selected_option = selected_option
        self.selected_index = selected_index
        self.save_list_selected = save_list_selected

    def start(self) -> Optional[Scene]:
        """
        See above
        """

        logger.info("Starting Scene: SelectSave")
        key = ""
        selected_index = self.selected_index
        selected_option = self.selected_option
        save_manager = SaveManager()
        saves = save_manager.saves
        current = saves[0]
        save_list_selected = self.save_list_selected
        while key != "\n":
            # setup
            title = " Save files "

            # get the save with the longest name
            # TODO: truncate names too long
            longest_name = len(title)
            for save in saves:
                name = save.data["name"]
                if len(name) > longest_name:
                    longest_name = len(name)

            save_start_y_pos = 3
            save_x_pos = 2

            self.clear()

            save_name_x_pos = longest_name + 3
            option_x_pos = save_name_x_pos + 2

            # show separator
            self.renderer.stdscr.vline(
                1, save_name_x_pos, curses.ACS_VLINE, self.renderer.max_y - 2  # type: ignore
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
            if save_list_selected:
                self.addinto(
                    save_x_pos - 1,
                    y_pos_selected,
                    selected_name,
                    curses.A_BOLD | curses.A_REVERSE,
                )
            else:
                self.addinto(
                    save_x_pos - 1,
                    y_pos_selected,
                    selected_name,
                    curses.A_DIM | curses.A_REVERSE,
                )

            # show options
            options = {
                1: "Load selected",
                2: "Rename selected",
                3: "Delete selected",
                4: "Create new",
            }
            options_positions_offsets = {1: 0, 2: 1, 3: 2, 4: 4}
            option_start_y_pos = 3

            self.addinto(option_x_pos, 1, " Actions ", curses.A_DIM | curses.A_REVERSE)

            for number, name in options.items():
                self.addinto(
                    option_x_pos,
                    option_start_y_pos + options_positions_offsets[number],
                    name,
                )

            # highlight current option
            highlighted_option = options[selected_option]
            highlighted_option = " " + highlighted_option.ljust(longest_name, " ")
            y_pos_selected_option = (
                option_start_y_pos + options_positions_offsets[selected_option]
            )
            if save_list_selected:
                self.addinto(
                    option_x_pos - 1,
                    y_pos_selected_option,
                    highlighted_option,
                    curses.A_DIM | curses.A_REVERSE,
                )
            else:
                self.addinto(
                    option_x_pos - 1,
                    y_pos_selected_option,
                    highlighted_option,
                    curses.A_BOLD | curses.A_REVERSE,
                )

            # show help
            helps = {
                1: "ENTER: Load save '{}'",
                2: "ENTER: Rename save '{}'",
                3: "ENTER: Delete save '{}'",
                4: "ENTER: Create new save",
            }
            help_text = helps[selected_option]
            help_text = help_text.format(name)
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
                if key == "KEY_DOWN":
                    if selected_option < 4:
                        selected_option += 1
                elif key == "KEY_UP":
                    if selected_option > 1:
                        selected_option -= 1
                else:
                    logger.warning("Unhandled key '%s'", key)

            logger.info("Selected save: '%s'", name)
            logger.info("Selected option: '%s'", selected_option)

        name = current.data["name"]
        if selected_option == 1:
            self.addinto_centred(20, "Loading '{}'...".format(name))

            self.state = current

            self.clear()
            self.addinto_all_centred("Done.")

            return StartComputer(self.renderer, self.state)
        if selected_option == 2:
            prompt_text = "New name for save '{}': ".format(name)
            new_name = self.prompt(
                round(self.renderer.max_x / 2) - 15 - round(len(prompt_text) / 2),
                round(self.renderer.max_y / 2),
                prompt_text,
            )
            save_manager.rename(current, new_name)
        elif selected_option == 3:
            confirmation_prompt = " Are you sure you want to delete the save '{}'? ".format(
                name
            )
            key = ""
            while key not in ("y", "n"):
                self.renderer.add_down_bar_text(
                    confirmation_prompt, color_pair=curses.A_REVERSE
                )
                self.renderer.add_down_bar_text(
                    " [y/n] ", 2, color_pair=curses.A_REVERSE
                )
                key = self.get_key()
                key = key.lower()
            if key == "y":
                self.addinto_all_centred("Deleting save {}...\n\t\t".format(name))
                save_manager.delete(current)

        elif selected_option == 4:
            return CorruptedLoginNewSave(self.renderer, self.state)
        else:
            logger.critical("Unhandled selected option: '%s'", selected_option)

        return SelectSave(
            self.renderer,
            self.state,
            selected_index,
            selected_option,
            save_list_selected,
        )

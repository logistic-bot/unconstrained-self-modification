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
        self.save_list_selected_index = save_list_selected

    def start(self) -> Optional[Scene]:
        """
        See above
        """

        logger.info("Starting Scene: SelectSave")

        save_list_title = " Save files "

        saves = self.get_saves()
        save_manager = SaveManager()

        selected_state = saves[0]

        acting_on_save_list = self.save_list_selected_index
        save_list_selected_index = self.selected_index
        selected_option = self.selected_option

        minimum_width = 30
        len_longest_name = self.get_len_longest_save(minimum_width)

        actions = {
            1: "Load selected",
            2: "Rename selected",
            3: "Delete selected",
            4: "Create new",
        }
        actions_positions_offsets = {1: 0, 2: 1, 3: 2, 4: 4}
        actions_start_y_pos = 3

        helps = {
            1: "ENTER: Load save '{}'",
            2: "ENTER: Rename save '{}'",
            3: "ENTER: Delete save '{}'",
            4: "ENTER: Create new save",
        }

        key = ""
        while key != "\n":
            self.clear()

            save_start_y_pos = 3
            save_x_pos = 2

            save_name_x_pos = len_longest_name + 3
            option_x_pos = save_name_x_pos + 2

            # show separator
            self.show_separator(save_name_x_pos)

            # show title
            self.show_save_list_title(save_list_title, save_name_x_pos)

            # show the save list
            save_names = [save.data["name"] for save in saves]
            self.draw_list(save_start_y_pos, save_x_pos, save_names)

            # highlight selected_state
            self.highlight_selected_save(
                acting_on_save_list,
                len_longest_name,
                save_list_selected_index,
                save_start_y_pos,
                save_x_pos,
                saves,
                selected_state,
            )

            # show actions
            self.show_action_title(option_x_pos)

            for number, name in actions.items():
                self.addinto(
                    option_x_pos,
                    actions_start_y_pos + actions_positions_offsets[number],
                    name,
                )

            # highlight selected_state option
            highlighted_option = actions[selected_option]
            highlighted_option = " " + highlighted_option.ljust(len_longest_name, " ")
            y_pos_selected_option = (
                actions_start_y_pos + actions_positions_offsets[selected_option]
            )
            if acting_on_save_list:
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
            self.show_help(helps, selected_option, selected_state)

            # handle key
            key = self.get_key()

            if key.lower() == "q":
                return None  # exit the game

            # select pane
            acting_on_save_list = self.select_pane(key)

            if acting_on_save_list:
                save_list_selected_index = self.handle_save_list_key(
                    key, save_list_selected_index, saves
                )
            else:
                selected_option = self.handle_actions_key(key, selected_option)

            name = selected_state.data["name"]
            logger.info("Selected save: '%s'", name)
            logger.info("Selected option: '%s'", selected_option)

        name = selected_state.data["name"]
        if selected_option == 1:  # Load game
            self.load_game(selected_state)
            return StartComputer(self.renderer, self.state)

        if selected_option == 2:  # Rename
            self.rename_game(selected_state)
        elif selected_option == 3: # Delete
            self.delete_game(selected_state)
        elif selected_option == 4: # New
            return CorruptedLoginNewSave(self.renderer, self.state)
        else:
            logger.critical("Unhandled selected option: '%s'", selected_option)

        # restart
        return SelectSave(
            self.renderer,
            self.state,
            save_list_selected_index,
            selected_option,
            acting_on_save_list,
        )

    def delete_game(self, selected_state):
        name = selected_state.data["name"]
        confirmation_prompt = " Are you sure you want to delete the save '{}'? ".format(name)

        key = ""
        while key not in ("y", "n"):
            self.renderer.add_down_bar_text(confirmation_prompt, color_pair=curses.A_REVERSE)
            self.renderer.add_down_bar_text(" [y/n] ", 2, color_pair=curses.A_REVERSE)

            key = self.get_key().lower()

        if key == "y":
            self.addinto_all_centred("Deleting save {}...".format(name))
            SaveManager().delete(selected_state)

    def rename_game(self, selected_state):
        name = selected_state.data["name"]

        prompt_text = "New name for save '{}': ".format(name)

        new_name = self.prompt(
            round(self.renderer.max_x / 2) - 15 - round(len(prompt_text) / 2),
            round(self.renderer.max_y / 2),
            prompt_text,
        )

        save_manager = SaveManager()
        save_manager.rename(selected_state, new_name)

    def load_game(self, selected_state):
        name = selected_state.data["name"]
        self.addinto_centred(20, "Loading '{}'...".format(name))
        self.state = selected_state
        self.clear()
        self.addinto_all_centred("Done.")

    def handle_actions_key(self, key, selected_option):
        if key == "KEY_DOWN":
            if selected_option < 4:
                selected_option += 1
        elif key == "KEY_UP":
            if selected_option > 1:
                selected_option -= 1
        else:
            logger.warning("Unhandled key '%s'", key)
        return selected_option

    def handle_save_list_key(self, key, save_list_selected_index, saves):
        if key == "KEY_DOWN":
            if save_list_selected_index < len(saves) - 1:
                save_list_selected_index += 1
        elif key == "KEY_UP":
            if save_list_selected_index > 0:
                save_list_selected_index -= 1
        else:
            logger.warning("Unhandled key '%s'", key)
        return save_list_selected_index

    def select_pane(self, key):
        if key == "KEY_RIGHT":
            return False
        elif key == "KEY_LEFT":
            return True

    def show_help(self, helps, selected_option, selected_state):
        name = selected_state.data["name"]
        help_text = helps[selected_option]
        help_text = help_text.format(name)
        self.renderer.add_down_bar_text(help_text, 0, curses.A_REVERSE)

    def show_action_title(self, option_x_pos):
        self.addinto(option_x_pos, 1, " Actions ", curses.A_DIM | curses.A_REVERSE)

    def highlight_selected_save(
        self,
        acting_on_save_list,
        len_longest_name,
        save_list_selected_index,
        save_start_y_pos,
        save_x_pos,
        saves,
        selected_state,
    ):
        selected_state = saves[save_list_selected_index]
        name = selected_state.data["name"]
        y_pos_selected = save_start_y_pos + save_list_selected_index
        selected_name = " " + name.ljust(len_longest_name + 1, " ")
        if acting_on_save_list:
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
        return name, selected_state

    def draw_list(self, start_y_pos, x_pos, items):
        for index, item in enumerate(items):
            self.addinto(x_pos, start_y_pos + index, item)

    def show_save_list_title(self, save_list_title, save_name_x_pos):
        title_start_x = round(save_name_x_pos / 2) - round(len(save_list_title) / 2)
        self.addinto(title_start_x, 1, save_list_title, curses.A_DIM | curses.A_REVERSE)

    def show_separator(self, x_pos):
        self.renderer.stdscr.vline(
            1, x_pos, curses.ACS_VLINE, self.renderer.max_y - 2  # type: ignore
        )

    def get_len_longest_save(self, min_len: int = 0) -> int:
        """
        Get the lenght of the name of the save that has the longest name
        :param min_len: The minimum length of the returned value.
        """
        # get the save with the longest name
        # TODO: truncate names too long
        longest_name = min_len
        for save in self.get_saves():
            name = save.data["name"]
            if len(name) > longest_name:
                longest_name = len(name)
        return longest_name

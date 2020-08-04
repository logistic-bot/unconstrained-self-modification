"""
This files contains the SelectSave scene, which allows the user to select a save that will then
be loaded.
"""

# TODO: This file is hideous. Refactor as soon as possible. Maybe try using some kind of GUI
#  framework?
# TODO: The todo items in the documentation note the items that should be computed inside the
#  function, not passed as an argument. This is not a complete list.

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
from typing import Optional, List, Dict

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

        key = ""
        while key != "\n":
            self.clear()
            selected_state = saves[save_list_selected_index]

            save_start_y_pos = 3
            save_x_pos = 2

            save_name_x_pos = len_longest_name + 3
            option_x_pos = save_name_x_pos + 2

            # show separator
            self.show_separator(save_name_x_pos)

            self.show_save_list(
                acting_on_save_list,
                len_longest_name,
                save_list_selected_index,
                save_list_title,
                save_name_x_pos,
                save_start_y_pos,
                save_x_pos,
                saves,
            )

            self.show_actions(
                acting_on_save_list,
                actions,
                actions_positions_offsets,
                actions_start_y_pos,
                len_longest_name,
                option_x_pos,
                selected_option,
            )

            # show help
            self.show_help(selected_option, selected_state)

            # handle key
            key = self.get_key()

            if key.lower() == "q":
                return None  # exit the game

            # select pane
            if key == "KEY_RIGHT":
                acting_on_save_list = False
            elif key == "KEY_LEFT":
                acting_on_save_list = True

            if acting_on_save_list:
                save_list_selected_index = self.handle_save_list_key(
                    key, save_list_selected_index, saves
                )
            else:
                selected_option = self.handle_actions_key(key, selected_option)

            name = selected_state.data["name"]
            logger.info("Selected save: '%s'", name)
            logger.info("Selected option: '%s'", selected_option)

        if selected_option == 1:  # Load game
            self.load_game(selected_state)
            return StartComputer(self.renderer, self.state)

        if selected_option == 2:  # Rename
            self.rename_game(selected_state)
        elif selected_option == 3:  # Delete
            self.delete_game(selected_state)
        elif selected_option == 4:  # New
            return CorruptedLoginNewSave(self.renderer, self.state)
        else:
            logger.critical("Unhandled selected option: '%s'", selected_option)

        if len(self.get_saves()) >= 1:
            # restart
            return SelectSave(
                self.renderer,
                self.state,
                save_list_selected_index,
                selected_option,
                acting_on_save_list,
            )
        else:
            return CorruptedLoginNewSave(self.renderer, self.state)

    def show_actions(
        self,
        acting_on_save_list: bool,
        actions: Dict[int, str],
        actions_positions_offsets: Dict[int, int],
        actions_start_y_pos: int,
        len_longest_name: int,
        option_x_pos: int,
        selected_option: int,
    ) -> None:
        """
        Show available actions
        :param acting_on_save_list: False if the action list is selected
        :param actions: A dict mapping action number to action description
        :param actions_positions_offsets: A dict mapping action numbers to action position
        offsets.
        :param actions_start_y_pos: The start y_pos of the action list
        :param len_longest_name: The length of the longest save name
        :param option_x_pos: x_pos of the action list
        :param selected_option: A number representing the action number that is currently selected.
        """
        # show actions
        self.show_action_title(option_x_pos)
        self.draw_actions(
            actions, actions_positions_offsets, actions_start_y_pos, option_x_pos
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

    def show_save_list(
        self,
        acting_on_save_list: bool,
        len_longest_name: int,
        save_list_selected_index: int,
        save_list_title: str,
        save_name_x_pos: int,
        save_start_y_pos: int,
        save_x_pos: int,
        saves: List[GameState],
    ) -> None:
        """
        Show the list of saved games.
        :param acting_on_save_list: True if the list of saved games is selected.
        :param len_longest_name: The length of the longest save name TODO
        :param save_list_selected_index: The index of the currently selected save.
        :param save_list_title: The title of the save list.
        :param save_name_x_pos: x_pos of the save list tile TODO
        :param save_start_y_pos: start y_pos of the save names
        :param save_x_pos: The x_pos of the save list
        :param saves: A list of GameStates to show in the list
        """
        # show save list title
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
        )

    def draw_actions(
        self,
        actions: Dict[int, str],
        actions_positions_offsets: Dict[int, int],
        actions_start_y_pos: int,
        option_x_pos: int,
    ) -> None:
        """
        Show the actions to the player
        :param actions: A dict mapping action numbers to actions string
        :param actions_positions_offsets: A dict mapping action numbers position offsets
        :param actions_start_y_pos: The start y_pos of the list
        :param option_x_pos: The x_pos of the list
        """
        for number, name in actions.items():
            self.addinto(
                option_x_pos,
                actions_start_y_pos + actions_positions_offsets[number],
                name,
            )

    def delete_game(self, selected_state: GameState) -> None:
        """
        Delete the currently selected game
        :param selected_state: The currently selected game
        """
        name = selected_state.data["name"]
        confirmation_prompt = " Are you sure you want to delete the save '{}'? ".format(
            name
        )

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

        self.renderer.add_down_bar_text(
            confirmation_prompt, color_pair=curses.A_REVERSE | curses.color_pair(1) | curses.A_BOLD
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
                    confirmation_prompt, color_pair=curses.A_REVERSE | curses.color_pair(1)
            )

        if key == "y":
            self.addinto_all_centred("Deleting save {}...".format(name))
            SaveManager().delete(selected_state)

    def rename_game(self, selected_state: GameState) -> None:
        """
        Rename the currently selected game
        :param selected_state: the currently selected game
        """
        name = selected_state.data["name"]

        prompt_text = "New name for save '{}': ".format(name)

        new_name = self.prompt(
            round(self.renderer.max_x / 2) - 15 - round(len(prompt_text) / 2),
            round(self.renderer.max_y / 2),
            prompt_text,
        )

        save_manager = SaveManager()
        save_manager.rename(selected_state, new_name)

    def load_game(self, selected_state: GameState) -> None:
        """
        Load the currently selected
        :param selected_state: The currently selected game
        """
        name = selected_state.data["name"]
        self.addinto_centred(20, "Loading '{}'...".format(name))
        self.state = selected_state
        self.clear()
        self.addinto_all_centred("Done.")

    @staticmethod
    def handle_actions_key(key: str, selected_option: int) -> int:
        """
        Handle up and down keys in the actions menu.

        read the doc for handle_save_list_key for more information

        :param key: The key to handle
        :param selected_option: The currently selected option number.
        :return: The new selected option
        """
        if key == "KEY_DOWN":
            if selected_option < 4:
                selected_option += 1
        elif key == "KEY_UP":
            if selected_option > 1:
                selected_option -= 1
        else:
            logger.warning("Unhandled key '%s'", key)
        return selected_option

    @staticmethod
    def handle_save_list_key(
        key: str, save_list_selected_index: int, saves: List[GameState]
    ) -> int:
        """
        Handle keys in the save list. If the up or the down key is pressed, increment or
        decrement save_list_selected_index if possible. The return value indicates which save was
        selected by the user.

        :param key: The key to handle
        :param save_list_selected_index: The index of the currently selected game in saves
        :param saves: A list of GameState objects displayed on the screen in the same order
        :return: The new save_list_selected_index.
        """
        if key == "KEY_DOWN":
            if save_list_selected_index < len(saves) - 1:
                save_list_selected_index += 1
        elif key == "KEY_UP":
            if save_list_selected_index > 0:
                save_list_selected_index -= 1
        else:
            logger.warning("Unhandled key '%s'", key)
        return save_list_selected_index

    def show_help(self, selected_option: int, selected_state: GameState) -> None:
        """
        Show the help message for the currently selected option and state.

        :param selected_option: The currently selected option number
        :param selected_state: The current selected state
        """
        helps = {
            1: "ENTER: Load save '{}'",
            2: "ENTER: Rename save '{}'",
            3: "ENTER: Delete save '{}'",
            4: "ENTER: Create new save",
        }
        name = selected_state.data["name"]
        help_text = helps[selected_option]
        help_text = help_text.format(name)
        self.renderer.add_down_bar_text(help_text, 0, curses.A_REVERSE)

    def show_action_title(self, option_x_pos: int) -> None:
        """
        Draw the title of action pane

        :param option_x_pos: x_pos of the title
        """
        self.addinto(option_x_pos, 1, " Actions ", curses.A_DIM | curses.A_REVERSE)

    def highlight_selected_save(
        self,
        acting_on_save_list: int,
        len_longest_name: int,
        save_list_selected_index: int,
        save_start_y_pos: int,
        save_x_pos: int,
    ) -> None:
        """
        Highlight the save that is currently selected.

        :param acting_on_save_list: Whether or not the save pane is currently selected. True if
        it is selected.
        :param len_longest_name: How wide the pane is
        :param save_list_selected_index: index of the currently selected save
        :param save_start_y_pos: At which y_pos does the save list start
        :param save_x_pos: At which x_pos does the save list start
        """
        saves = self.get_saves()
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

    def draw_list(self, start_y_pos: int, x_pos: int, items: List[str]) -> None:
        """
        Show a list of items on the screen, one item under the other.

        :param start_y_pos: at which y_pos should the list start
        :param x_pos: at which x_pos should the list be
        :param items: the list to display
        """
        for index, item in enumerate(items):
            self.addinto(x_pos, start_y_pos + index, item)

    def show_save_list_title(self, save_list_title: str, save_name_x_pos: int) -> None:
        """
        Show the title of save list
        :param save_list_title: Title to show
        :param save_name_x_pos: x_pos of the save list title
        """
        title_start_x = round(save_name_x_pos / 2) - round(len(save_list_title) / 2)
        self.addinto(title_start_x, 1, save_list_title, curses.A_DIM | curses.A_REVERSE)

    def show_separator(self, x_pos: int) -> None:
        """
        Show a separator at the given x_pos
        :param x_pos: the x_pos of the separator
        """
        self.renderer.stdscr.vline(
            1, x_pos, curses.ACS_VLINE, self.renderer.max_y - 2  # type: ignore
        )

    def get_len_longest_save(self, min_len: int = 0) -> int:
        """
        Get the length of the name of the save that has the longest name
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

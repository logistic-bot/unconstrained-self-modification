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

from src.core.scene import FullScreenScene, Scene
from src.core.state.save_manager import SaveManager
from src.scenes.start_computer import StartComputer


class SelectSave(FullScreenScene):
    """
    Ask the user to select a save, then load it.
    """

    def start(self) -> Scene:
        """
        See above
        """
        title = " Select a save to load... "

        save_manager = SaveManager()
        saves = save_manager.saves

        # get the save with the longest name
        longest_name = len(title)
        for save in saves:
            name = save.data["name"]
            if len(name) > longest_name:
                longest_name = len(name)

        selected_index = 0
        save_start_y_pos = 5
        key = ""
        current = saves[0]
        while key != "\n":
            self.clear()

            # show title
            self.addinto_centred(3, title, 0, 0, curses.A_DIM | curses.A_REVERSE)

            # show the list
            for save_index, save in enumerate(saves):
                name = save.data["name"]
                self.addinto_centred(
                    save_start_y_pos + save_index,
                    name.ljust(longest_name, " "),
                    0,
                    0,
                    curses.A_BOLD,
                )

            # highlight current
            current = saves[selected_index]
            name = current.data["name"]
            self.addinto_centred(
                save_start_y_pos + selected_index,
                name.upper().ljust(longest_name, " "),
                0,
                0,
                curses.A_BOLD | curses.A_BLINK,
            )

            # show help
            self.addinto(
                1,
                self.renderer.max_y - 1,
                " ENTER: load save '{}' ({})".format(
                    name, current.data["user"]["username"]
                ),
                curses.A_REVERSE,
            )

            # handle key
            key = self.get_key()
            if key == "KEY_DOWN":
                if selected_index < len(saves) - 1:
                    selected_index += 1
            if key == "KEY_UP":
                if selected_index > 0:
                    selected_index -= 1

        self.addinto_centred(20, "Loading '{}'...".format(current.data["name"]))

        self.state.load_from_save(current)

        self.clear()
        self.addinto_all_centred("Done.")

        return StartComputer(self.renderer, self.state)

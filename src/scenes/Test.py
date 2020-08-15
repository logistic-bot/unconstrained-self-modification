"""
This FullScreenScene is responsible for showing the game's title and startup messages.
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
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

from typing import Any

from src.core.scene import FullScreenScene
from src.core.user_interface import ListRenderer


class TestScene(FullScreenScene):

    """
    This scene is called at the start of the game, in engine.py
    """

    def start(self) -> Any:  # pylint: disable=R1711
        saves = ListRenderer(
            self.renderer, 1, 1, ["save 1", "save 245", "save 34861"], True, margin=1
        )
        actions = ListRenderer(
            self.renderer,
            saves.actual_width,
            1,
            ["Load567890", "Rename", "Delete", "New"],
            True,
            margin=1,
        )
        tmp = ListRenderer(
            self.renderer,
            saves.actual_width + actions.actual_width + 10,
            1,
            ["tmp567890", "tmpRename", "tmpDelete", "tmpNew"],
            True,
            margin=1,
        )

        tmp.set_selected(False)

        key = ""
        while key != "q":
            key = self.get_key()

            saves.check_input(key)
            actions.check_input(key)
            tmp.check_input(key)

            if key == "s":
                saves.selected = not saves.selected
                tmp.selected = not tmp.selected

            saves.draw()
            actions.draw()
            tmp.draw()

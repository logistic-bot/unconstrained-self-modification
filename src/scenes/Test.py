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
from src.core.user_interface import TreeListRenderer


class TestScene(FullScreenScene):

    """
    This scene is called at the start of the game, in engine.py
    """

    def start(self) -> Any:  # pylint: disable=R1711

        # treelist = TreeListRenderer(self.renderer, 5, 5 ,[[list,list2,list3,["",""]])
        treelist = TreeListRenderer(
            self.renderer, 5, 5, [["Test", "Tryce"], ["Action1", "Action2"]]
        )

        key = ""
        while key != "q":
            treelist.draw()
            key = self.get_key()

            treelist.check_input(key)

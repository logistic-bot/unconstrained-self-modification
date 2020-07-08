"""
Game engine
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

from src.core import render
from src.scenes import startup


class Engine:  # pylint: disable=R0903
    """
    Game engine
    """

    def __init__(self) -> None:
        self.renderer = render.CursesRenderer()

    def start(self) -> None:
        """
        Start the game
        """
        try:
            current_scene = startup.StartupScene(self.renderer)
            while current_scene is not None:
                current_scene = current_scene.start()
        finally:
            self.renderer.tear_down()
            print("The game exited.")

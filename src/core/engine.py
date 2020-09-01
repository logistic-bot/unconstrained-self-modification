"""
Game engine
-----------
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


import logging
from typing import Optional

from src.core import render
from src.core.scene import Scene
from src.core.state import game_state
from src.scenes.startup import StartupScene

logger = logging.getLogger(__name__)


class Engine:  # pylint: disable=R0903
    """
    Game engine
    """

    def __init__(self) -> None:
        self.renderer = render.CursesRenderer()
        self.game_state = game_state.GameState()

        logger.info("Created game engine.")

    # noinspection PyBroadException
    def start(self) -> None:
        """
        Start the game
        """

        logger.info("Starting game")

        try:
            # current_scene: Optional[Scene] = TestScene(self.renderer, self.game_state)
            current_scene: Optional[Scene] = StartupScene(
                self.renderer, self.game_state
            )

            while current_scene is not None:
                logger.info("Current scene: %s", current_scene)

                current_scene = current_scene.start()

        except KeyboardInterrupt:
            logger.critical("KeyboardInterrupt", exc_info=True)
        except:  # noqa: E722 pylint: disable=W0702
            logger.critical("An exception occurred.", exc_info=True)

        finally:
            logger.info("Tearing down curses, and exiting game")

            self.renderer.tear_down()
            print("The game exited.")

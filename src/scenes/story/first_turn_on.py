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

import logging
from typing import Any

from src.animations.story import first_turn_on
from src.core.scene import FullScreenScene

logger = logging.getLogger(__name__)


class FirstTurnOnStory(FullScreenScene):
    """
    This scene is called at the start of the game, in engine.py
    """

    def start(self) -> Any:  # pylint: disable=R1711
        """
        Shows a copyright notice and the game's title.

        If there is at least one save, show the save select Scene, in other cases, show the
        StartComputer scene.
        """
        logger.info("Starting Story: 'FirstTurnOnStory'")

        self.clear()
        self.sleep_key(0.7)
        animation = first_turn_on.create_animation(self.renderer)
        animation.start()

        for x_pos in range(1, self.renderer.max_x, 7):
            for y_pos in range(1, self.renderer.max_y - 1):
                if (x_pos + 6) < self.renderer.max_x:
                    self.renderer.addtext(x_pos, y_pos, "       ")
                    self.renderer.addtext(x_pos, y_pos, "FASM-4")
                    self.sleep_key(0.001)
                else:
                    break

        self.sleep_key(1)
        return FirstTurnOnStory(self.renderer, self.state)

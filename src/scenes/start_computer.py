"""
This scene is for the start of the game, this computer is the first that the user can use.
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

import curses
import logging
from pathlib import Path

from src.animations import start_computer_bios, start_computer_boot
from src.core.scene import FullScreenScene
from src.scenes.ether_industries_login import EtherIndustriesLogin

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOGO_START_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "1"
LOGO_DONE_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "2"

logger = logging.getLogger(__name__)

with LOGO_START_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_START = "\n".join(logo)

with LOGO_DONE_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_DONE = "\n".join(logo)


class StartComputer(FullScreenScene):
    """
    The first computer the user can use.
    """

    def start(self) -> EtherIndustriesLogin:  # pylint: disable=R0914
        """
        Shows the init sequence of the first computer.

        :return:
        """
        logger.info("Starting Scene: StartComputer")

        self.clear()
        animation = start_computer_bios.create_animation(self.renderer)
        y_pos = animation.start()

        font_logo = (
            curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK
        )
        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        animation = start_computer_boot.create_animation(self.renderer)
        animation.start(y_pos + 1)  # leave a blank line

        return EtherIndustriesLogin(self.renderer, self.state)

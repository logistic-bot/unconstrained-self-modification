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
from pathlib import Path
from time import sleep

from src.core.scene import Scene

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOGO_START_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "1"
LOGO_DONE_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "2"

with LOGO_START_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_START = "\n".join(logo)

with LOGO_DONE_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_DONE = "\n".join(logo)


class StartComputer(Scene):
    """
    The first computer the user can use.
    """

    def start(self) -> None:
        """
        Shows the init sequence of the first computer.

        :return:
        """
        # init colors
        font_logo = (
            curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK
        )
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        font_info = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        font_good = curses.color_pair(2) | curses.A_BOLD
        font_working = font_info | curses.A_BLINK | curses.A_REVERSE
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        font_bad = curses.color_pair(3) | curses.A_BOLD

        self.addinto(1, 1, "EtherBIOS v2.3.1 initialising...", font_info)
        self.addinto(45, 1, "WORKING", font_working)
        sleep(1.5)
        self.addinto(1, 2, "CPU 0: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 3, "CPU 1: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 4, "CPU 2: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 5, "CPU 3: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.5)
        self.addinto(1, 6, "GPU 0: Ether Industries UltraText")
        sleep(0.3)
        self.addinto(45, 1, "[DONE] ", font_good)
        sleep(0.1)

        self.addinto(1, 7, "STARTING SELF-TEST", font_info)
        self.addinto(45, 7, "WORKING", font_working)
        sleep(1.5)
        self.addinto(
            1, 8, "WARNING No graphics available, starting in text mode", font_bad
        )
        sleep(0.7)
        self.addinto(45, 7, "[DONE] ", font_good)
        self.addinto(1, 9, "Booting from disk 0...", font_info)

        sleep(1.5)

        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        self.get_key()

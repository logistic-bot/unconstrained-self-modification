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

from src.core.render.boot_animation import (BootAnimation, BootAnimationStage, StyledText,
                                            BootAnimationStageStep, )
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

    def start(self) -> None:  # pylint: disable=R0914
        # TODO: Move the animation definiton to own file.
        # TODO: Programming language name: Parcel-3
        """
        Shows the init sequence of the first computer.

        :return:
        """
        # init colors
        font_logo = (
            curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK
        )
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        # text definition
        init = StyledText(self.renderer, "EtherBIOS v2.3.1 initialising...", 1)
        self_test = StyledText(self.renderer, "STARTING SELF-TEST...", 1)
        cpu0 = StyledText(
            self.renderer, "CPU 0: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0
        )
        cpu1 = StyledText(
            self.renderer, "CPU 1: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0
        )
        cpu2 = StyledText(
            self.renderer, "CPU 2: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0
        )
        cpu3 = StyledText(
            self.renderer, "CPU 3: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0
        )
        gpu = StyledText(self.renderer, "GPU 0: Ether Industries UltraText", 0)
        gpu_warning = StyledText(
            self.renderer,
            "WARNING: No graphics available, starting in text mode",
            3,
            bold=True,
        )
        boot = StyledText(self.renderer, "Booting from disk 0...", 1)
        progress = StyledText(self.renderer, "WORKING", 1, blinking=True, inverted=True)
        finished = StyledText(self.renderer, "DONE", 2, bold=True)

        # step list definition
        cpus = [cpu0, cpu1, cpu2, cpu3]
        cpu_steps = [BootAnimationStageStep(cpu, delay=0.3) for cpu in cpus]
        gpu_step = BootAnimationStageStep(gpu, delay=0.3)
        bios_steps = cpu_steps + [gpu_step]
        self_test_steps = [BootAnimationStageStep(gpu_warning, delay=0.7)]

        # stage definitions
        bios_stage = BootAnimationStage(
            self.renderer, init, progress, finished, bios_steps, 1.5
        )
        self_test_stage = BootAnimationStage(
            self.renderer, self_test, progress, finished, self_test_steps
        )
        boot_stage = BootAnimationStage(self.renderer, boot)

        # BootAnimation works.
        animation = BootAnimation(
            self.renderer, [bios_stage, self_test_stage, boot_stage], delay=1.5
        )
        animation.start()

        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        self.get_key()

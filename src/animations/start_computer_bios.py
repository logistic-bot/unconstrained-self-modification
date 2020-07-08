"""
This is the boot animation from the first computer
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

# init colors
import curses

from src.core.boot_animation.boot_animation import StyledText, Step, Stage, BootAnimation
from src.core.render import CursesRenderer


def create_animation(renderer: CursesRenderer) -> BootAnimation:
    """create a boot animation and returns it"""
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    # text definition
    init = StyledText(renderer, "EtherBIOS v2.3.1 initialising...", 1)
    self_test = StyledText(renderer, "STARTING SELF-TEST...", 1)
    cpu0 = StyledText(renderer, "CPU 0: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0)
    cpu1 = StyledText(renderer, "CPU 1: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0)
    cpu2 = StyledText(renderer, "CPU 2: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0)
    cpu3 = StyledText(renderer, "CPU 3: Ether Industries Pulse 32 Cores 128 bit 9MHz", 0)
    gpu = StyledText(renderer, "GPU 0: Ether Industries UltraText", 0)
    gpu_warning = StyledText(renderer, "WARNING: No graphics available, starting in text mode", 3,
                             bold=True, )
    boot = StyledText(renderer, "Booting from disk 0...", 1)
    progress = StyledText(renderer, "WORKING", 1, blinking=True, inverted=True)
    finished = StyledText(renderer, "DONE", 2, bold=True)

    # step list definition
    cpus = [cpu0, cpu1, cpu2, cpu3]
    cpu_steps = [Step(cpu, delay=0.3) for cpu in cpus]
    gpu_step = Step(gpu, delay=0.3)
    bios_steps = cpu_steps + [gpu_step]
    self_test_steps = [Step(gpu_warning, delay=0.7)]

    # stage definitions
    bios_stage = Stage(renderer, init, progress, finished, bios_steps, 1.5)
    self_test_stage = Stage(renderer, self_test, progress, finished, self_test_steps)
    boot_stage = Stage(renderer, boot)

    # BootAnimation works.
    animation = BootAnimation(renderer, [bios_stage, self_test_stage, boot_stage], delay=1.5)
    return animation

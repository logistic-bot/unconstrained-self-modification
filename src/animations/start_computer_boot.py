"""
This is the boot animation for the first computer. It will play after the bios animation for the
first computer.
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

from src.core.boot_animation.boot_animation import (BootAnimation, InfoStage, SimultaneousStage, )
from src.core.boot_animation.stage import Stage
from src.core.boot_animation.step import Step
from src.core.boot_animation.styled_text import StyledText
from src.core.render import CursesRenderer


def create_animation(renderer: CursesRenderer) -> BootAnimation:
    """create a boot animation and returns it"""
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # info
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # progress
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # good
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # bad

    progress = StyledText(renderer, "IN PROGRESS", 5, blink=True, invert=True)
    # finished = StyledText(renderer, ["[", "OK", "]"], 2, bold=True)
    finished = StyledText(
        renderer,
        [
            StyledText(renderer, ["[", " "], 0, bold=True),
            StyledText(renderer, ["  ", "OK", "  "], 2, bold=True),
            StyledText(renderer, [" ", "]"], 0, bold=True),
        ],
        2,
        bold=True,
    )
    success = StyledText(
        renderer,
        [
            StyledText(renderer, ["[", " "], 0, bold=True),
            StyledText(renderer, "PASSED", 2, bold=True),
            StyledText(renderer, [" ", "]"], 0, bold=True),
        ],
        0,
        bold=True,
    )
    # warning = StyledText(renderer, "WARNING", 3, bold=True, blinking=True)

    greet = StyledText(renderer, "Ether Industries EtherOS v6.2.4", 0)
    ether_copyright = StyledText(
        renderer, "Copyright (C) 2024-2052 Ether Industries, Inc.", 0
    )
    cpu_test_0 = StyledText(renderer, "Testing cpu 0", 4)
    cpu_test_1 = StyledText(renderer, "Testing cpu 1", 4)
    cpu_test_2 = StyledText(renderer, "Testing cpu 2", 4)
    cpu_test_3 = StyledText(renderer, "Testing cpu 3", 4)
    gpu_test = StyledText(renderer, "Testing gpu 0", 4)
    compiler = StyledText(renderer, "Loading parcel 3 compiler", 4)
    text_mode = StyledText(renderer, "Starting text interface", 4)

    greet_steps = [Step(greet), Step(ether_copyright)]
    test_step = [cpu_test_0, cpu_test_1, cpu_test_2, cpu_test_3, gpu_test]

    test_stage_tmp = [
        Stage(renderer, step, progress, success, delay=1) for step in test_step
    ]
    for stage in test_stage_tmp:
        stage.status_x = 40

    greet_stage = InfoStage(renderer, greet_steps, 0.7, 1)
    test_stage = SimultaneousStage(renderer, test_stage_tmp, 1.5, 0.5, 0.7)
    compiler_stage = Stage(renderer, compiler, progress, finished, delay=1.5)
    compiler_stage.status_x = 40
    final_stage = Stage(renderer, text_mode, progress, finished, delay=1.5)
    final_stage.status_x = 40

    animation = BootAnimation(
        renderer, [greet_stage, test_stage, compiler_stage, final_stage]
    )
    return animation

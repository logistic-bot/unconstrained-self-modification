"""
Say that the login file is corrupted and a new superuser will be created
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
import logging

from src.core.boot_animation.boot_animation import BootAnimation, InfoStage
from src.core.boot_animation.step import Step
from src.core.boot_animation.styled_text import StyledText
from src.core.render import CursesRenderer

logger = logging.getLogger(__name__)


def create_animation(renderer: CursesRenderer) -> BootAnimation:
    """create a boot animation and returns it"""
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    greet = StyledText(
        renderer, "Ether Industry EtherOS v6.2.4 (black-hole-01) (tty1)", 0
    )
    error = StyledText(
        renderer,
        [
            StyledText(renderer, "[ether-login c198762] ", dim=True),
            StyledText(renderer, "ERROR", 3, blink=True),
            StyledText(renderer, ": User database file corrupted."),
        ],
    )
    info = StyledText(
        renderer,
        [
            StyledText(renderer, "[ether-login c198762] ", dim=True),
            StyledText(renderer, "INFO", 1),
            StyledText(renderer, ": Creating new superuser."),
        ],
    )

    steps = [Step(text, delay=0.2) for text in [greet, error, info]]
    stage = InfoStage(renderer, steps, delay=0.7)
    animation = BootAnimation(renderer, [stage])

    logger.info(
        "Created boot_animation: EtherIndustriesPasswordCorrupt: '%s'", animation
    )

    return animation

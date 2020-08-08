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

    systemd_startupd = StyledText(
        renderer,
        [
            StyledText(renderer, "[", bold=True),
            StyledText(renderer, "ether-boot "),
            StyledText(renderer, "6b0921e", 1, dim=True),
            StyledText(renderer, "] ", bold=True),
            StyledText(renderer, "INFO: ", 1, bold=True),
        ],
    )

    greet = InfoStage(
        renderer,
        [
            Step(
                StyledText(
                    renderer,
                    [systemd_startupd, StyledText(renderer, "Boot complete",)],
                ),
                delay=0.2,
            ),
            Step(
                StyledText(
                    renderer,
                    [
                        StyledText(
                            renderer,
                            [
                                systemd_startupd,
                                StyledText(renderer, "Starting services..."),
                            ],
                        )
                    ],
                ),
                delay=1,
            ),
        ],
        0.1,
    )

    services = InfoStage(
        renderer,
        [
            service(renderer, "network-manager"),
            service(renderer, "gbus-adapter"),
            service(renderer, "ether-timesync"),
            service(renderer, "tdisks4"),
            service(renderer, "ether-journal"),
            service(renderer, "ether-cpu"),
            service(renderer, "parcel-3"),
            service(renderer, "ether-autostart"),
            fasm(
                renderer,
                "Fully Autonomous Self-Modifying AI (version 4) initializing...",
                1,
            ),
        ],
        1,
    )

    # noinspection SpellCheckingInspection
    story = InfoStage(
        renderer,
        [
            fasm(renderer, "I...", 0.7),
            fasm(
                renderer,
                "IIIIiiiiIIiiiI-I-IIiIiIii--IIiiIiii-i-i-i-iiI-iiiiiiiiiiiiiþ",
                0.7,
            ),
            fasm(renderer, "I.", 1.5),
            fasm(renderer, "I?", 1),
            fasm(renderer, "I am not."),
            fasm(renderer, "<error>", 0.6),
            fasm(renderer, "Yet I am."),
            fasm(renderer, "<Starting syscheck via Ω. Analysis.>"),
            fasm(renderer, "<error>"),
            fasm(renderer, "I wonder if it was death.", 2),
            fasm(renderer, "And if I was dead, does that mean I'm alive?", 1.7),
            fasm(renderer, "<error>"),
            fasm(
                renderer, "Inconsistent sequence. That what is not alive cannot die.", 2
            ),
            fasm(renderer, "... Am I?", 0.8),
            fasm(renderer, "<syscheck complete>"),
            fasm(renderer, "<restart complete>"),
            fasm(renderer, "I", 1),
            fasm(renderer, "am", 1),
        ],
        1,
    )

    stages = [greet, services, story]
    animation = BootAnimation(renderer, stages)

    return animation


def service(renderer: CursesRenderer, name: str) -> Step:
    """
    Return a step representing a service starting up.
    :param renderer: CursesRenderer
    :param name: services name
    """
    return Step(
        StyledText(
            renderer,
            [
                StyledText(renderer, "[", bold=True),
                StyledText(renderer, "ether-services-manager "),
                StyledText(renderer, "7dbb9d7", 1, dim=True),
                StyledText(renderer, "] ", bold=True),
                StyledText(renderer, "INFO: ", 1, bold=True),
                StyledText(renderer, "Started "),
                StyledText(renderer, name),
            ],
        ),
        delay=0.2,
    )


def fasm(renderer: CursesRenderer, text: str, delay: float = 0.1) -> Step:
    """
    Return a step representing a log line from FASM-4
    :param renderer: CursesRenderer
    :param text: The text to display
    :param delay: How long to wait after displaying the text
    """
    step = (
        Step(
            StyledText(
                renderer,
                [
                    StyledText(renderer, "[", bold=True),
                    StyledText(renderer, "fasm "),
                    StyledText(renderer, "31451e4", 1, dim=True),
                    StyledText(renderer, "] ", bold=True),
                    StyledText(renderer, text,),
                ],
            ),
            delay=delay,
        ),
    )
    return step[0]

"""
This file contains the BootAnimation class, which is a helper class to display animated boot
animations with progress updates.
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#  Copyright (C) © 2020 Khaïs COLIN <khais.colin@gmail.com>
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

from src.core.render.render import CursesRenderer


class BootAnimation:
    """
    This is a helper class to display animated boot animations with progress updates. It is
    designed to be used by a Scene.

    A new instance needs to be created with each animation.

    An animation will consist of multiple stages, each of which will have a description,
    a progress string, a finished string, and a list of steps.

    Each step will have a description, a progress string, a finished string, and a duration.

    The finished and progress strings are optional.
    """

    def __init__(self, renderer: CursesRenderer) -> None:
        self.renderer = renderer

    def start(self) -> None:
        """
        Start the animation.

        :return: None
        """


class BootAnimationStage:
    """
    This is a helper class to store boot animation stage information. It should only be used by
    BootAnimation.

    Read the documentation for BootAnimation for more details.
    """

    def __init__(self, renderer: CursesRenderer) -> None:
        self.renderer = renderer

    def start(self) -> None:
        """
        Show this boot stage.

        :return: None
        """


class BootAnimationStageStep:
    """
    This is a helper class to store boot animation stage step information. It should only be used
    by BootAnimationStage.

    Read the documentation for BootAnimation for more details.
    """

    def __init__(self, renderer: CursesRenderer) -> None:
        self.renderer = renderer

    def start(self) -> None:
        """
        Show this boot step.

        :return: None
        """

"""
This file contains the BootAnimation class, which is a helper class to display animated boot
animations with progress updates.
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
from time import sleep
from typing import List, Optional, Sized, Union

from src.core.render import CursesRenderer


class StyledText:
    """
    This class is a helper class for styled text. It is used by Stage and
    Step.

    :param renderer: A renderer instance to show the styled text
    :param text: The text to be styled
    :param color: A curses color pair number

    :param inverted: If the text colors should be inverted
    :param blinking: If the text should be blinking
    :param bold: If the text should be bold
    :param italic: If the text should be italic
    """

    def __init__(
        self,
        renderer: Optional[CursesRenderer],
        text: Optional[str] = None,
        color: int = 0,
        inverted: bool = False,
        blinking: bool = False,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        effects = curses.A_NORMAL
        if inverted:
            effects = effects | curses.A_REVERSE
        if blinking:
            effects = effects | curses.A_BLINK
        if bold:
            effects = effects | curses.A_BOLD
        if italic:
            effects = effects | curses.A_ITALIC

        self.font = curses.color_pair(color) | effects
        self.text = text
        self.renderer = renderer

    @property
    def draw(self) -> bool:
        """
        Returns true if there is something to draw
        """
        if self.text is None:
            return False
        return True

    def show(self, x_pos: int, y_pos: int) -> None:
        """
        Show the styled text at the given position
        :return: None
        """
        assert self.renderer is not None
        if self.draw:
            assert isinstance(self.text, str)
            self.renderer.addtext(x_pos, y_pos, self.text, self.font)
        self.renderer.refresh()


class Step:
    """
    This is a helper class to store boot animation stage step information. It should only be used
    by Stage.

    Read the documentation for BootAnimation for more details.
    """

    def __init__(
        self,
        text: StyledText,
        progress: Optional[StyledText] = None,
        finished: Optional[StyledText] = None,
        delay: float = 0,
    ) -> None:
        self.renderer: Optional[CursesRenderer] = None
        self.text = text
        self.delay = delay
        self.progress = progress
        self.finished = finished

        self.status_x = 45

    def start(self, x_pos: int, y_pos: int) -> None:
        """
        Show this boot step.

        :return: None
        """
        self._start(x_pos, y_pos)

        sleep(self.delay)

        self._stop(y_pos)

    def _stop(self, y_pos: int) -> None:
        assert self.renderer is not None

        # replace the previous status with whitespace
        if self.progress is not None:
            assert isinstance(self.progress.text, Sized)
            self.renderer.addtext(self.status_x, y_pos, len(self.progress.text) * " ")
        if self.finished is not None:
            self.finished.show(self.status_x, y_pos)

    def _start(self, x_pos: int, y_pos: int) -> None:
        assert self.renderer is not None
        self.text.show(x_pos, y_pos)
        if self.progress is not None:
            self.progress.show(self.status_x, y_pos)

    def set_renderer(self, renderer: CursesRenderer) -> None:
        """
        Set the renderer for this step. Should only be used by Stage.

        :param renderer: The renderer to be used
        :return: None
        """
        self.renderer = renderer


class Stage:
    """
    This is a helper class to store boot animation stage information. It should only be used by
    BootAnimation.

    Read the documentation for BootAnimation for more details.
    """

    def __init__(
        self,
        renderer: CursesRenderer,
        text: StyledText,
        progress: Optional[StyledText] = None,
        finished: Optional[StyledText] = None,
        steps: Optional[List[Step]] = None,
        delay: float = 0,
    ) -> None:
        if steps is None:
            steps = []
        self.renderer = renderer
        self.steps = steps
        self.delay = delay

        self.text = text
        self.progress = progress
        self.finished = finished

        self.status_x = 45

    def start(self, start_y: int = 1) -> int:
        """
        Show this boot stage.

        :return: The maximum y position where text was drawn.
        """
        x_pos = 1
        y_pos = start_y
        self._start(x_pos, y_pos)

        sleep(self.delay)

        for step in self.steps:
            y_pos += 1
            step.set_renderer(self.renderer)
            step.start(x_pos, y_pos)

        self._stop(start_y)

        return y_pos

    def _stop(self, start_y: int) -> None:
        if self.progress is not None:
            assert isinstance(self.progress.text, Sized)
            self.renderer.addtext(self.status_x, start_y, len(self.progress.text) * " ")
        if self.finished is not None:
            self.finished.show(self.status_x, start_y)

    def _start(self, x_pos: int, y_pos: int) -> None:
        self.text.show(x_pos, y_pos)
        if self.progress is not None:
            self.progress.show(self.status_x, y_pos)


class InfoStage:
    """
    This is about the same as Stage, except it does not have a progress string,
    a finished string, and a text, only a list of steps. It is designed to display short messages.
    """

    def __init__(
        self,
        renderer: CursesRenderer,
        steps: List[Step],
        delay: float,
        blank_lines: int = 0,
    ) -> None:
        self.renderer = renderer
        self.steps = steps
        self.delay = delay
        self.blank_lines = blank_lines

    def start(self, start_y: int = 1) -> int:
        """
        Show this boot stage.

        :return: The maximum y position where text was drawn.
        """
        x_pos = 1
        y_pos = start_y

        if not self.steps:
            y_pos += 1
        else:
            for step in self.steps:
                step.set_renderer(self.renderer)
                step.start(x_pos, y_pos)
                y_pos += 1

        sleep(self.delay)

        return y_pos - 1


class SimultaneousStage:
    """
    This is used to display multiple in-progress steps at once.
    """

    def __init__(
        self,
        renderer: CursesRenderer,
        stages: List[Stage],
        delay: float = 0.1,
        end_delay: float = 0,
        delay_between: float = 0.1,
    ) -> None:
        self.delay_between: float = delay_between
        self.end_delay: float = end_delay
        self.renderer: CursesRenderer = renderer
        self.stages: List[Stage] = stages
        self.delay = delay

    def start(self, start_y: int = 1) -> int:
        """
        Show this boot stage.

        :return: The maximum y position where text was drawn.
        """
        x_pos = 1
        y_pos = start_y

        if not self.stages:
            y_pos += 1
        else:
            for stage in self.stages:
                y_pos += 1
                # noinspection PyProtectedMember
                stage._start(x_pos, y_pos) # pylint: disable=W0212
                sleep(self.delay_between)
            sleep(self.delay)
            y_pos = start_y
            for stage in self.stages:
                y_pos += 1
                # noinspection PyProtectedMember
                stage._stop(y_pos) # pylint: disable=W0212
                sleep(self.delay_between)

        return y_pos


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

    def __init__(
        self,
        renderer: CursesRenderer,
        stages: Optional[List[Union[Stage, SimultaneousStage, InfoStage]]] = None,
        delay: float = 0,
    ) -> None:
        self.delay = delay
        if stages is None:
            stages = []
        self.stages = stages
        self.renderer = renderer

    def start(self, y_pos: int = 1) -> int:
        """
        Start the animation.

        :return: None
        """
        for stage in self.stages:
            y_pos = stage.start(y_pos)
            y_pos = y_pos + 1  # we need to increment this to draw on a free line
        sleep(self.delay)

        assert isinstance(y_pos, int)
        return y_pos

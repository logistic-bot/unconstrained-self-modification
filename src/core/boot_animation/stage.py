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

from time import sleep
from typing import Optional, List, Sized

from src.core.boot_animation.step import Step
from src.core.boot_animation.styled_text import StyledText
from src.core.render import CursesRenderer


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

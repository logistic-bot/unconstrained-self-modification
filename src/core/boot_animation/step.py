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
from typing import Optional, Sized

from src.core.boot_animation.styled_text import StyledText
from src.core.render import CursesRenderer


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

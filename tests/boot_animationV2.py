from src.core.render import CursesRenderer
from typing import List, Optional, Union
from tests.stagesV2 import Stage
from time import sleep

class BootAnimation:

    renderer : CursesRenderer
    delay = 1

    def __init__(self, renderer : CursesRenderer, stages: Optional[List[Union[Stage]]] = None):
        self.renderer = renderer
        self.stages = stages

    def start(self, y_pos: int = 1) -> int:
        """
        Start the animation.

        :return: None
        """
        for stage in self.stages:
            y_pos = stage.start(y_pos,5)
            y_pos += 1  # we need to increment this to draw on a free line
        sleep(self.delay)
        return y_pos
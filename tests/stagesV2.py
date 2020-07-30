from src.core.boot_animation.styled_text import StyledText
from typing import List
from time import sleep
from src.core.render import CursesRenderer

# TODO: Create STEPS Class

class Stage:

    def __init__(self, renderer: CursesRenderer, text: List[StyledText], delay: List[float], progress: List[StyledText]):
        self.renderer = renderer
        self.text = text
        self.delay = delay
        self.progress = progress

    def start(self, start_y: int = 1, start_x: int = 1):
        x_pos = start_x
        y_pos = start_y
        status_x: int = 0

        for t in range(len(self.text)):
            if len(self.text[t]) > status_x:
                status_x = len(self.text[t])

        status_x += start_x+1

        for t in range(len(self.text)):
            self.text[t].show(x_pos, y_pos)
            for p in range(len(self.progress)):
                self.progress[p].show(status_x, y_pos)

                sleep(self.delay[p])

                self.renderer.addtext(status_x, start_y, len(self.progress[p].text) * " ")
        return y_pos
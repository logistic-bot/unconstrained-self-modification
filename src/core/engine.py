"""
Game engine
"""

from src.core.render import render


class Engine:
    """
    Game engine
    """
    def __init__(self) -> None:
        self.renderer = render.CursesRenderer()

    def start(self) -> None:
        """
        Start the game
        """
        try:
            self.main_loop()
        finally:
            self.renderer.tear_down()

    def main_loop(self) -> None:
        """
        Main game loop
        """
        while True:
            self.step()

    def step(self) -> None:
        """
        Make one step in the simulation
        """
        self.render()
        self.handle_io()

    def render(self) -> None:
        """
        Render to the console
        """
        self.renderer.render()

    def handle_io(self) -> None:
        """
        Handle keypresses
        """
        self.wait_keypress()

    def wait_keypress(self) -> None:
        """
        Wait for the user to press a key
        """
        self.renderer.wait_keypress()

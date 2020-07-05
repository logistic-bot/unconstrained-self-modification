"""
Game engine
"""

from src.core.render import render
from src.scenes import startup


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
            startup_scene = startup.StartupScene(self.renderer)
            startup_scene.start()
        finally:
            self.renderer.tear_down()
            print("The game exited.")

    def main_loop(self) -> None:
        """
        Main game loop
        """
        key = ""
        while key != "q":
            self.step()
            key = self.get_key()

    def get_key(self) -> str:
        """
        Wait for a key to be pressed, and return a string representing it. For more
        documentation, see the documentation for CursesRenderer.get_key().
        :return:
        """
        return self.renderer.get_key()

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

    def wait_keypress(self) -> None:
        """
        Wait for the user to press a key
        """
        self.renderer.wait_keypress()

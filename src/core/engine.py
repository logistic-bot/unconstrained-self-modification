"""
Game engine
"""

from src.core.render import render
from src.scenes import startup


class Engine:  # pylint: disable=R0903
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
            current_scene = startup.StartupScene(self.renderer)
            while current_scene is not None:
                current_scene = current_scene.start()
        finally:
            self.renderer.tear_down()
            print("The game exited.")

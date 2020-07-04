"""
This Scene is responsible for showing the game's title and startup messages.
"""

from pathlib import Path
from typing import Optional

from src.core.scene import Scene

STARTUP_MESSAGE_PATH = Path(__file__).parent.absolute() / "STARTUP"

with open(STARTUP_MESSAGE_PATH, "r") as f:
    STARTUP_MESSAGE = f.read()


class StartupScene(Scene):
    """
    This scene is called at the start of the game, in engine.py
    """
    def start(self) -> Optional[Scene]:  # pylint: disable=R1711
        """
        Shows a copyright notice and the game's title.
        """
        self.clear()
        self.sleep_key(0.3)
        self.addinto_all_centred(STARTUP_MESSAGE, delay=0.1, pager_delay=0)
        self.sleep_key(50)

        return None

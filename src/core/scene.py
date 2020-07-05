"""
This file implements the Scene class, which contains convenience methods for all Scenes.
"""

from src.core.render.render import CursesRenderer


class Scene:
    """
    The base class for all Scenes, contains convenience methods.
    """
    def __init__(self, renderer: CursesRenderer) -> None:
        self.renderer = renderer

    def sleep_key(self, delay: float) -> bool:
        """
        Wait until a key is pressed, or the delay is exceeded.

        For more documentation, see CursesRenderer.wait_keypress_delay()

        :param delay: How many seconds to wait for a key press
        """
        if delay == 0:
            return False

        key = self.renderer.wait_keypress_delay(delay)
        return key == -1

    def addinto_centred(self, y_pos: int, text: str, delay: float = 0, pager_delay: float = 2) -> \
            bool:
        """
        Add a text into, centered vertically, with optional delay between lines.

        If the terminal is not tall enough, the text will be paged. In that case, the parameter
        pager_delay is used to delay each page.

        :param y_pos: The y position where the text should be displayed
        :param text: The text to be displayed
        :param delay: Delay between each line
        :param pager_delay: Delay between each page
        :return: True if the text was skipped, False otherwise
        """
        line_count = len(text.splitlines())

        if y_pos < 1:
            y_pos = 1

        if line_count > self.renderer.max_y - 2:  # -2 for the borders
            max_lines = self.renderer.max_y - 2
            all_lines = text.splitlines()
            next_lines = "\n".join(all_lines[:max_lines])
            remainder = "\n".join(all_lines[max_lines - 5:])
            skip = self.addinto_centred(y_pos, next_lines, delay, pager_delay)

            skip_all = not self.sleep_key(pager_delay)
            self.clear()

            if skip:
                delay = 0

            if skip_all:
                return delay == 0

            self.addinto_centred(y_pos, remainder, delay, pager_delay)
            return delay == 0

        for idx, line in enumerate(text.splitlines()):
            line = line.strip()

            self.renderer.addtext((round(self.renderer.max_x / 2) - round(len(line) / 2)),
                                  y_pos + idx, line)

            self.refresh()

            if line == "":
                continue

            full_delay = self.sleep_key(delay)

            if not full_delay:
                delay = 0

        self.sleep_key(pager_delay)
        return delay == 0

    def addinto_all_centred(self, text: str, delay: float = 0, pager_delay: float = 2) -> bool:
        """
        Adds a text into the canvas, completely centred.

        For more documentation, see Scene.addinto_centred()

        :param text: The text to be displayed
        :param delay: How many seconds to wait between each line
        :param pager_delay: How many seconds to wait between each page.
        """
        line_count = len(text.splitlines())
        return self.addinto_centred(round(self.renderer.max_y / 2) - round(line_count / 2), text,
                                    delay,
                                    pager_delay)

    def refresh(self) -> None:
        """
        Refresh the screen, making sure that all modified characters are displayed correctly.
        :return:
        """
        self.renderer.refresh()

    def clear(self) -> None:
        """
        Clear the screen, and redraw the borders.
        """
        self.renderer.clear_screen()

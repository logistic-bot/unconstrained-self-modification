from time import sleep
from pathlib import Path

STARTUP_MESSAGE_PATH = Path(__file__).parent.absolute() / "STARTUP"

with open(STARTUP_MESSAGE_PATH, "r") as f:
    STARTUP_MESSAGE = f.read()


class StartupScene:
    def __init__(self, renderer):
        self.renderer = renderer

    def start(self):
        self.clear()
        self.addinto_allcentred(STARTUP_MESSAGE, delay=0.2, pager_delay=0)
        self.sleep_key(2)

    def sleep_key(self, delay, inc=0.01):
        if delay == 0: return False
        key = self.renderer.wait_keypress_delay(delay)
        return True if key == -1 else False

    def addinto_allcentred(self, text, delay=0, pager_delay=2):
        line_count = len(text.splitlines())
        self.addinto_centred(round(self.renderer.max_y / 2) - line_count, text, delay, pager_delay)

    def addinto_centred(self, y_pos, text, delay=0, pager_delay=2):
        line_count = len(text.splitlines())

        if y_pos < 1:
            y_pos = 1

        if line_count > self.renderer.max_y - 2: # -2 for the borders
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
                return

            self.addinto_centred(y_pos, remainder, delay, pager_delay)
            return

        for idx, line in enumerate(text.splitlines()):
            line = line.strip()

            self.renderer.addtext((round(self.renderer.max_x / 2) - round(len(line) / 2)), y_pos + idx, line)

            self.refresh()

            if line == "":
                continue

            full_delay = self.sleep_key(delay)

            if not full_delay:
                delay = 0

        self.sleep_key(pager_delay)
        return True if delay == 0 else False

    def refresh(self):
        self.renderer.refresh()

    def clear(self):
        self.renderer.clear_screen()
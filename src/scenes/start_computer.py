import curses
from pathlib import Path
from time import sleep

from src.core.scene import Scene

PROJECT_ROOT = Path(__file__).parent.parent.parent.absolute()
LOGO_START_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "1"
LOGO_DONE_PATH = PROJECT_ROOT / "assets" / "ether_industries" / "2"

with LOGO_START_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_START = "\n".join(logo)

with LOGO_DONE_PATH.open("r") as f:
    logo = [line.strip() for line in f]
    LOGO_DONE = "\n".join(logo)


class StartComputer(Scene):
    def start(self):
        # init colors
        font_logo = curses.color_pair(0) | curses.A_ITALIC | curses.A_BOLD | curses.A_BLINK
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        font_info = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        font_good = curses.color_pair(2) | curses.A_BOLD
        font_working = font_info | curses.A_BLINK | curses.A_REVERSE
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        font_bad = curses.color_pair(3) | curses.A_BOLD


        self.addinto(1, 1, "EtherBIOS v2.35.16 initialising...", font_info)
        self.addinto(45, 1, "WORKING", font_working)
        sleep(1.5)
        self.addinto(1, 2, "CPU 0: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 3, "CPU 1: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 4, "CPU 2: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.3)
        self.addinto(1, 5, "CPU 3: Ether Industries Pulse 32 Cores 128 bit 9MHz")
        sleep(0.5)
        self.addinto(1, 6, "GPU 0: Ether Industries UltraText")
        sleep(0.3)
        self.addinto(45, 1, "[DONE] ", font_good)
        sleep(0.1)

        self.addinto(1, 7, "STARTING SELF-TEST", font_info)
        self.addinto(45, 7, "WORKING", font_working)
        sleep(1.5)
        self.addinto(1, 8, "WARNING No graphics available, starting in text mode", font_bad)
        sleep(0.7)
        self.addinto(45, 7, "[DONE] ", font_good)
        self.addinto(1, 9, "Booting from disk 0...", font_info)

        sleep(1.5)

        self.addinto_all_centred(LOGO_START, 0.05)
        self.addinto_all_centred(LOGO_DONE, color_pair=font_logo)

        self.get_key()

    def addinto(self, x_pos, y_pos, text, color_pair=0):
        self.renderer.addtext(x_pos, y_pos, text, color_pair)
        self.refresh()

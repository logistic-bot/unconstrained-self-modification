#!/usr/bin/env python
from src.core.engine import Engine

def main():
    engine = Engine()
    engine.start()

    # char = ""
    # while char != "q":
    #     win_y, win_x = stdscr.getmaxyx()
    #
    #     # render
    #     stdscr.clear_screen()
    #
    #     stdscr.move(1, 1)
    #     stdscr.addstr("Mind-Control based roguelike.")
    #     stdscr.move(2, 1)
    #     stdscr.addstr("All coordinates are given in the form (y, x) in compliance with curses api.")
    #     stdscr.move(3, 1)
    #     stdscr.addstr("Player location: ({}, {}) Window size: ({}, {}).".format(player_y, player_x, win_y, win_x))
    #
    #     stdscr.move(player_y, player_x)
    #     stdscr.addch("@")
    #
    #     stdscr.box()
    #
    #     stdscr.refresh()
    #
    #
    #     # input
    #     char = stdscr.getkey()
    #
    #     if char == "KEY_UP":
    #         player_y -= 1
    #     elif char == "KEY_DOWN":
    #         player_y += 1
    #     elif char == "KEY_RIGHT":
    #         player_x += 1
    #     elif char == "KEY_LEFT":
    #         player_x -= 1
    #     else:
    #         stdscr.addstr(char)

if __name__ == "__main__":
    main()

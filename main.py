#!/usr/bin/env python

"""
Run this file to start the game
"""

from src.core.engine import Engine


def main() -> None:
    """
    main
    """
    engine = Engine()
    engine.start()

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

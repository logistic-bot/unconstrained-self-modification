#!/usr/bin/env python

"""
Run this file to start the game
"""

# ------------------------------------------------------------------------------
#  This file is part of Universal Sandbox.
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

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

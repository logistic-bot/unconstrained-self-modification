#!/usr/bin/env python
import curses

from src.core.render import render as render

def main():
    stdscr = render.setup()

    player_x = 10
    player_y = 10

    char = ""
    while char != "q":
        # render
        stdscr.clear()

        stdscr.move(0, 0)
        stdscr.addstr("Mind-Control based roguelike")

        stdscr.move(player_y, player_x)
        stdscr.addch("@")

        stdscr.refresh()


        # input
        char = stdscr.getkey()

        if char == "KEY_UP":
            player_y -= 1
        elif char == "KEY_DOWN":
            player_y += 1
        elif char == "KEY_RIGHT":
            player_x += 1
        elif char == "KEY_LEFT":
            player_x -= 1
        else:
            stdscr.addstr(char)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        render.tear_down()
        print("An exception was uncatched, and crashed the main game. This is a bug.")
        print("The error message is:", e)
        print("Please file a bug report and attache the WHOLE output of the game.")
        print("Also make sure to describe what you were doing, and what operating system you have.")
        print()
        raise e
    finally:
        render.tear_down()


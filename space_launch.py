from __future__ import annotations

from curses import wrapper


def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, f"10 divided by {v} is {10/v}")

        stdscr.refresh()
        stdscr.getkey()


wrapper(main)

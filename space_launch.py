from __future__ import annotations

import argparse
import curses
import time
from collections.abc import Sequence

rb = [
    "   I",
    "  /o\\",
    "  | |",
    "  | |",
    " /[_]\\",
    "   A",
    "  ( )",
    "   )",
    "  ( )",
]


def space_launch(stdscr: curses.window) -> None:

    lines = curses.LINES
    for y in range(lines, 0, -1):
        # Clear screen
        stdscr.clear()
        for i, line in enumerate(rb):
            try:
                stdscr.addstr(y + i, 0, line)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(0.04)


def my_wrapper(func, /, *args, **kwds):
    """like curses.wrapper but without starting color"""
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(1)
        stdscr.leaveok(True)

        return func(stdscr, *args, **kwds)
    finally:
        # Set everything back to normal
        if "stdscr" in locals():
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="space_launch")
    _ = parser.parse_args(argv)
    my_wrapper(space_launch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

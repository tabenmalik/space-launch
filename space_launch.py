from __future__ import annotations

import argparse
import curses
import time
from collections.abc import Callable
from collections.abc import Sequence
from itertools import count
from typing import NamedTuple


class Frame(NamedTuple):
    hold: float
    image: tuple[str, ...]


FRAMES: tuple[Frame, ...] = (
    Frame(
        hold=0.02,
        image=(
            "   I",
            "  /o\\",
            "  | |",
            "  | |",
            " /[_]\\",
            "   A",
            "  ( )",
            "   )",
            "  ( )",
        ),
    ),
    Frame(
        hold=0.02,
        image=(
            "   I",
            "  /o\\",
            "  | |",
            "  | |",
            " /[_]\\",
            "   A",
            "   (",
            "  ( )",
            "   )",
        ),
    ),
)


def space_launch(stdscr: curses.window) -> None:

    lines = curses.LINES
    for y in count():
        curses.update_lines_cols()
        # Clear screen
        stdscr.clear()
        half = curses.COLS // 2
        for frame in FRAMES:
            for i, line in enumerate(frame.image):
                try:
                    stdscr.addstr(lines - y + i, half - 4, line)
                except curses.error:
                    pass
            if lines - y + i < 0:
                return

            stdscr.refresh()
            time.sleep(frame.hold)


def my_wrapper(func: Callable[[curses.window], None], /) -> None:
    """like curses.wrapper but without starting color"""
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.leaveok(True)

        return func(stdscr)
    finally:
        # Set everything back to normal
        if "stdscr" in locals():
            stdscr.keypad(False)
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

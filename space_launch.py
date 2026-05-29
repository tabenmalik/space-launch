from __future__ import annotations

import argparse
import contextlib
import curses
import time
from collections.abc import Generator
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


def space_launch(stdscr: curses.window, frames: tuple[Frame, ...]) -> None:

    lines = curses.LINES
    for y in count():
        curses.update_lines_cols()
        # Clear screen
        stdscr.clear()
        half = curses.COLS // 2
        for frame in frames:
            for i, line in enumerate(frame.image):
                try:
                    stdscr.addstr(lines - y + i, half - 4, line)
                except curses.error:
                    pass
            if lines - y + i < 0:
                return

            stdscr.refresh()
            time.sleep(frame.hold)


@contextlib.contextmanager
def screen_init() -> Generator[curses.window]:
    """like curses.wrapper but without starting color"""
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(True)
        stdscr.leaveok(True)

        yield stdscr
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

    with screen_init() as stdscr:
        space_launch(stdscr, FRAMES)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

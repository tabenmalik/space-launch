from __future__ import annotations

import argparse
import contextlib
import curses
import time
from collections.abc import Generator
from collections.abc import Sequence


Frame = tuple[str, ...]


FRAMES: tuple[Frame, ...] = (
    (
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
    (
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
)


def space_launch(stdscr: curses.window, frames: tuple[Frame, ...]) -> None:

    lines = curses.LINES
    y = 0
    while True:
        for frame in frames:
            curses.update_lines_cols()
            stdscr.clear()
            half = curses.COLS // 2
            for i, line in enumerate(frame):
                try:
                    stdscr.addstr(lines - y + i, half - 4, line)
                except curses.error:
                    pass
            y += 1
            stdscr.refresh()
            time.sleep(0.06)
        if lines - y + i < 0:
            break


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

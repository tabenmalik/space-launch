from __future__ import annotations

import argparse
import curses
from collections.abc import Sequence


def space_launch(stdscr: curses.window) -> None:
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i - 10
        stdscr.addstr(i, 0, f"10 divided by {v} is {10/v}")

        stdscr.refresh()
        stdscr.getkey()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="space_launch")
    _ = parser.parse_args(argv)
    curses.wrapper(space_launch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

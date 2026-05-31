from __future__ import annotations

import argparse
import contextlib
import curses
import json
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


def space_launch(
    stdscr: curses.window,
    frames: tuple[Frame, ...],
    rate: float = 0.04,
) -> None:
    lines = curses.LINES
    y = 0
    while True:
        for frame in frames:
            curses.update_lines_cols()
            stdscr.erase()
            half = curses.COLS // 2
            for i, line in enumerate(frame):
                try:
                    stdscr.addstr(lines - y + i, half - 4, line)
                except curses.error:
                    pass
            y += 1
            stdscr.refresh()
            time.sleep(rate)
        if lines - y + i < 0:
            break


def load_animation(path: str) -> tuple[Frame, ...]:
    with open(path) as fp:
        data = json.load(fp)

    return tuple(map(tuple, data))


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

    # possibly temporary args while I figure out the ascii animation
    parser.add_argument("--animation")
    parser.add_argument("--rate", type=float, default=0.04)

    args = parser.parse_args(argv)

    if args.animation:
        frames = load_animation(args.animation)
    else:
        frames = FRAMES

    with screen_init() as stdscr:
        space_launch(stdscr, frames, args.rate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

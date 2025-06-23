#!/usr/bin/env python3
"""Fetch Advent of Code input text files."""

from __future__ import annotations

import subprocess
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path
import sys


class Args(Namespace):
    """Parsed CLI Arguments."""

    day: int | None
    """Day to fetch"""
    cookie: str | None
    """Cookie to use"""


def parse_args() -> Args:
    """Parse CLI Arguments."""
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    day = max((int(d.name[3:]) for d in Path.cwd().glob("day*")), default=None)
    parser.add_argument("day", type=int, help="Day to fetch", nargs="?", default=day)
    parser.add_argument("--cookie", help="Auth cookie. Otherwise, `auth.txt` is used")
    return parser.parse_args(namespace=Args())


def fetch(day: int, cookie: str | None = None) -> None:
    """Fetch the input for a given day, optionally using the given cookie.

    If the cookie is not given, a local `auth.txt` file is read
    """
    if cookie is None:
        with Path("auth.txt").open("r", encoding="utf8") as fid:
            cookie = fid.read().strip("\n")
    tgt = Path("inputs")
    tgt.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "curl",
            f"https://adventofcode.com/2021/day/{day}/input",
            "-H",
            f"Cookie: session={cookie}",
            "-o",
            tgt.joinpath(f"day{day:02d}.txt").resolve(),
            "-s",
        ],
        check=True,
    )


if __name__ == "__main__":
    args = parse_args()
    if args.day is None:
        print("Day is required", file=sys.stderr)
        sys.exit(1)
    fetch(args.day, args.cookie)

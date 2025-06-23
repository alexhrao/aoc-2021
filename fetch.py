#!/usr/bin/env python3
"""Fetch Advent of Code input text files."""

from __future__ import annotations

import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path


def parse_args() -> Namespace:
    """Parse CLI Arguments."""
    parser = ArgumentParser()
    parser.add_argument("day", type=int, help="Day to fetch")
    parser.add_argument("--cookie", help="Auth cookie. Otherwise, `auth.txt` is used")
    return parser.parse_args()


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
        check=False,
    )


if __name__ == "__main__":
    args = parse_args()
    fetch(args.day, args.cookie)

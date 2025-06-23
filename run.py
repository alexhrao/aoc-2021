#!/usr/bin/env python3
"""Run Advent of Code submissions for a given day."""

from __future__ import annotations

import re
import subprocess
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from statistics import mean
from time import process_time_ns
from typing import Callable

from fetch import fetch
from setup import SUFFIX_LANGS, Language

ENTRY_PAT = re.compile(r"^(\w+)-(\w+)-day\d+$")
"""Pattern that a directory is expected to follow."""

type Sample = tuple[int, int]
"""A single time sample."""


class Args(Namespace):
    """CLI Arguments."""

    day: int
    """Day to run"""
    warmup_rounds: int
    """Number of warmup rounds to execute"""
    num_rounds: int
    """Number of rounds over which to average"""


def parse_args() -> Args:
    """Parse CLI arguments."""
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    day = max((int(d.name[3:]) for d in Path.cwd().glob("day*")), default=None)

    if day is None:
        print("No days available to execute", file=sys.stderr)
        sys.exit(1)

    parser.add_argument(
        "day",
        type=int,
        help="Day to run",
        nargs="?",
        default=day,
    )
    parser.add_argument(
        "--warmup-rounds",
        "-w",
        type=int,
        help="Number of tries to warm up the runner",
        default=1,
    )
    parser.add_argument(
        "--num-rounds",
        "-n",
        type=int,
        help="Number of rounds to run; the result is the average",
        default=1,
    )
    args = parser.parse_args(namespace=Args())
    args.num_rounds = max(args.num_rounds, 1)
    args.warmup_rounds = max(args.warmup_rounds, 0)
    return args


def run_py(d: Path) -> Sample:
    """Run the given path as Python, returning the combined time."""
    # Create a runner
    start = process_time_ns()
    # Use the python venv
    subprocess.run(
        [Path(".venv", "bin", "python3"), "main.py", "1"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    p1 = process_time_ns() - start
    start = process_time_ns()
    # Use the python venv
    subprocess.run(
        [Path(".venv", "bin", "python3"), "main.py", "2"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p1, process_time_ns() - start


def run_go(d: Path) -> Sample:
    """Run the given path as a go module, returning the combined time.

    This builds the module before running it, so build times aren't included
    """
    subprocess.run(
        ["go", "build", "."],
        cwd=d,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    start = process_time_ns()
    subprocess.run(
        ["go", "run", ".", "--", "1"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    p1 = process_time_ns() - start
    start = process_time_ns()
    subprocess.run(
        ["go", "run", ".", "--", "2"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p1, process_time_ns() - start


def run_ts(d: Path) -> Sample:
    """Run the given path as a typescript script, returning the combined time.

    This compiles before running it, so compilation times aren't included
    """
    subprocess.run(
        ["npx", "tsc"],
        cwd=d,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return run_js(d)


def run_js(d: Path) -> Sample:
    """Run the given path as a node.js script, returning the combined time."""
    start = process_time_ns()
    subprocess.run(
        ["node", "index.js", "--", "1"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    p1 = process_time_ns() - start
    start = process_time_ns()
    subprocess.run(
        ["node", "index.js", "--", "2"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p1, process_time_ns() - start


def run_rs(d: Path) -> Sample:
    """Run the given path as a cargo crate, returning the combined time.

    This builds the crate in release mode before running it, so compilation time
    isn't included in the returned value
    """
    subprocess.run(
        ["cargo", "build", "--release", "--quiet"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Now run it and time it
    start = process_time_ns()
    subprocess.run(
        ["cargo", "run", "--release", "--quiet", "--", "1"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    p1 = process_time_ns() - start
    start = process_time_ns()
    subprocess.run(
        ["cargo", "run", "--release", "--quiet", "--", "2"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return p1, process_time_ns() - start


def summarize(times: dict[Language, dict[str, list[Sample]]]) -> None:
    """Summarize the combined times."""
    # Keyed by lang, then by name
    for lang in sorted(times.keys()):
        users = times[lang]
        print(f"{SUFFIX_LANGS[lang]}:")
        if len(users) == 0:
            print(" == No Submissions ==")
            continue
        for user, parts in users.items():
            p1 = int(mean(p[0] for p in parts))
            p2 = int(mean(p[1] for p in parts))
            print(f"  * {user} ({p1 / 1000000}ms, {p2 / 1000000}ms)")


if __name__ == "__main__":
    args = parse_args()
    day = Path(f"day{args.day:02d}")
    if not day.exists():
        print(f"There are no attempts for day {args.day}", file=sys.stderr)
        sys.exit(1)
    fetch(args.day)
    times: dict[Language, dict[str, list[Sample]]] = {}
    print(f"Taking samples for day {args.day}")
    for entry in day.iterdir():
        match = ENTRY_PAT.fullmatch(entry.name)
        if match is None:
            print(f"Invalid entry '{entry.name}'", file=sys.stderr)
            sys.exit(1)
        [lang, user] = match.groups()
        runner: Callable[[Path], Sample]
        if lang == "py":
            runner = run_py
        elif lang == "go":
            runner = run_go
        elif lang == "ts":
            runner = run_ts
        elif lang == "js":
            runner = run_js
        elif lang == "rs":
            runner = run_rs
        else:
            print(f"Unknown language '{lang}'; skipping", file=sys.stderr)
            continue
        if lang not in times:
            times[lang] = {}
        for _ in range(args.warmup_rounds):
            runner(entry)
        times[lang][user] = [runner(entry) for _ in range(args.num_rounds)]

    print(f"Results for day {args.day}")
    summarize(times)

#!/usr/bin/env python3
"""Run Advent of Code submissions, picking winners and losers."""

import subprocess
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from time import process_time_ns

from fetch import fetch
from setup import Language


def parse_args() -> Namespace:
    """Parse CLI arguments."""
    parser = ArgumentParser()
    parser.add_argument("day", type=int, help="Day to run")
    parser.add_argument(
        "--warmup-rounds",
        type=int,
        help="Number of tries to warm up the runner",
        default=0,
    )
    return parser.parse_args()


def run_py(d: Path) -> int:
    """Run the given path as Python, returning the combined time."""
    # Create a runner
    start = process_time_ns()
    # Use the python venv
    subprocess.run(
        [Path(".venv", "bin", "python3"), "main.py"],
        check=False,
        cwd=d,
    )
    return process_time_ns() - start


def run_go(d: Path) -> int:
    """Run the given path as a go module, returning the combined time.

    This builds the module before running it, so build times aren't included
    """
    subprocess.run(
        ["go", "build", "."],
        cwd=d,
        check=True,
    )
    start = process_time_ns()
    subprocess.run(
        ["go", "run", "."],
        check=False,
        cwd=d,
    )
    return process_time_ns() - start


def run_ts(d: Path) -> int:
    """Run the given path as a typescript script, returning the combined time.

    This compiles before running it, so compilation times aren't included
    """
    subprocess.run(
        ["npx", "tsc"],
        cwd=d,
        check=True,
    )
    return run_js(d)


def run_js(d: Path) -> int:
    """Run the given path as a node.js script, returning the combined time."""
    start = process_time_ns()
    subprocess.run(
        ["node", "index.js"],
        check=False,
        cwd=d,
    )
    return process_time_ns() - start


def run_rs(d: Path) -> int:
    """Run the given path as a cargo crate, returning the combined time.

    This builds the crate in release mode before running it, so compilation time
    isn't included in the returned value
    """
    subprocess.run(
        ["cargo", "build", "--release", "--quiet"],
        check=True,
        cwd=d,
    )
    # Now run it and time it
    start = process_time_ns()
    subprocess.run(
        ["cargo", "run", "--release", "--quiet"],
        check=False,
        cwd=d,
    )
    return process_time_ns() - start


def summarize(times: dict[Language, dict[str, int]]) -> None:
    """Summarize the combined times, picking a winner and a loser."""
    # Keyed by lang, then by name
    for lang, users in times.items():
        print(f"{lang}:")
        if len(users) == 0:
            print(" == No Submissions ==")
            continue
        bundles = sorted(users.items(), key=lambda u: u[1])
        print(f"Winner: {bundles[0][0]} ({bundles[0][1] / 1000000000}s)")
        for user, time in bundles[1:]:
            print(f"Loser: {user} ({time / 1000000000}s)")


if __name__ == "__main__":
    args = parse_args()
    fetch(args.day)
    day = Path(f"day{args.day:02d}")
    times: dict[Language, dict[str, int]] = {}
    for lang in day.iterdir():
        if lang.name == "py":
            runner = run_py
        elif lang.name == "go":
            runner = run_go
        elif lang.name == "ts":
            runner = run_ts
        elif lang.name == "js":
            runner = run_js
        elif lang.name == "rs":
            runner = run_rs
        else:
            print(f"Unknown language '{lang.name}'", file=sys.stderr)
            sys.exit(1)
        times[lang.name] = {}
        for user in lang.iterdir():
            for _ in range(args.warmup_rounds + 1):
                times[lang.name][user.name] = runner(user)

    summarize(times)

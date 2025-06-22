#!/usr/bin/env python3

from argparse import ArgumentParser
import subprocess
from pathlib import Path

def parser():
    parser = ArgumentParser()
    parser.add_argument("day", type=int, help="Day to fetch")
    parser.add_argument("user", choices=["ahr", "ukr"], help="User to fetch for")
    parser.add_argument("--cookie", help="Auth cookie. Otherwise, `auth.txt` is used")
    return parser.parse_args()

if __name__ == "__main__":
    args = parser()
    if args.cookie is None:
        with Path("auth.txt").open("r", encoding="utf8") as fid:
            args.cookie = fid.read().strip("\n")
    tgt = Path("inputs", args.user)
    tgt.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "curl",
            f"https://adventofcode.com/2021/day/{args.day}/input",
            "-H", f"Cookie: session={args.cookie}",
            "-o", tgt.joinpath(f"day{args.day:02d}.txt").resolve(),
            "-s",
        ],
    )
#!/usr/bin/env python3
"""Set up a new directory for an attempt."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from getpass import getuser
from pathlib import Path
from typing import Callable, Literal

type Language = Literal["rs", "py", "go", "js", "ts"]
"""An allowed programming language suffix"""

SUFFIXES: list[Language] = ["go", "js", "py", "rs", "ts"]
"""All the allowed suffixes"""

LANG_SUFFIXES: dict[str, Language] = {
    "Rust": "rs",
    "Python": "py",
    "Go": "go",
    "JavaScript": "js",
    "TypeScript": "ts",
}
"""Programming language names mapped to their standardized suffix."""

SUFFIX_LANGS: dict[Language, str] = {
    "rs": "Rust",
    "py": "Python",
    "go": "Go",
    "js": "JavaScript",
    "ts": "TypeScript",
}
"""Language file suffixes mapped to their standard name"""


class Args(Namespace):
    """Parsed CLI Arguments."""

    day: int
    """Day to set up."""
    lang: Language
    """Language to use."""
    user: Literal["ahr", "ukr"]
    """User who is making the attempt."""


def parse_args() -> Args:
    """Parse CLI Arguments."""
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("day", type=int, help="Day you want to setup, starting with 1")
    parser.add_argument(
        "lang",
        type=str.lower,
        choices=SUFFIXES,
        help="Language you want to use",
    )
    parser.add_argument(
        "user",
        choices=["ahr", "ukr"],
        help="Who are you",
        default="ahr" if getuser().startswith("al") else "ukr",
    )

    return parser.parse_args(namespace=Args())


def setup_py(d: Path, day: int) -> None:
    """Set up the directory as a Python3 script."""
    subprocess.run(["python3", "-m", "venv", ".venv"], check=True, cwd=d)
    with d.joinpath("main.py").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "#!/usr/bin/env python3\n",
                f'"""Python implementation for day {day:02d}."""\n',
                "\n",
                "from sys import argv\n\ndef part1():\n",
                "    pass\n",
                "\n",
                "\n",
                "def part2():\n",
                "    pass\n",
                "\n",
                'if __name__ == "__main__":\n',
                '    if len(argv) < 2 or argv[1] == "1":\n'
                "        print('Part 1')\n    part1()\n",
                '    if len(argv) < 2 or argv[1] == "2":\n'
                "        print('Part 2')\n    part2()\n",
            ],
        )
        st = os.fstat(fid.fileno())
        os.fchmod(fid.fileno(), st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/.venv\n*.pyc\n__pycache__\n")


def setup_go(d: Path, day: int) -> None:
    """Set up the directory as a go module."""
    subprocess.run(
        ["go", "mod", "init", f"day{day:02d}"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    with d.joinpath("main.go").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "package main\n",
                "\n",
                "import (\n",
                '\t"fmt"\n',
                '\t"os"\n',
                ")\n",
                "\n",
                "func part1() {}\n",
                "\n",
                "func part2() {}\n",
                "\n",
                "func main() {\n",
                '\tif len(os.Args) < 2 || os.Args[1] == "1" {\n',
                '\t\tfmt.Println("Part 1")\n',
                "\t\tpart1()\n",
                "\t}\n",
                '\tif len(os.Args) < 2 || os.Args[1] == "2" {\n',
                '\t\tfmt.Println("Part 2")\n',
                "\t\tpart2()\n",
                "\t}\n",
                "}\n",
            ],
        )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write(f"/day{day:02d}\n")


def setup_js(d: Path, day: int, ext: str | None = "js") -> None:
    """Set up the directory as a node.js script."""
    subprocess.run(
        ["npm", "init", "-y"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath("package.json").open("r", encoding="utf8") as fid:
        pkg = json.load(fid)
    pkg["name"] = f"day{day:02d}"
    pkg["scripts"]["start"] = "node index.js"
    with d.joinpath("package.json").open("w", encoding="utf8") as fid:
        json.dump(pkg, fid, indent=4)
    # Add node typings so VSC knows this is a node project
    subprocess.run(
        ["npm", "install", "--save-dev", "@types/node"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath(f"index.{ext}").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "function part1() {}\n",
                "\n",
                "function part2() {}\n",
                "\n",
                'if (process.argv.length < 2 || process.argv[1] === "1") {\n',
                '    console.log("Part 1");\n',
                "    part1();\n",
                "}\n",
                "\n",
                'if (process.argv.length < 2 || process.argv[1] === "2") {\n',
                '    console.log("Part 2");\n',
                "    part2();\n",
                "}\n",
            ],
        )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/node_modules\n")


def setup_ts(d: Path, day: int) -> None:
    """Set up the directory as a Typescript (to node.js) script."""
    # Start as if just vanilla JS
    setup_js(d, day, "ts")
    # Fix up the start script to use TSC
    with d.joinpath("package.json").open("r", encoding="utf8") as fid:
        pkg = json.load(fid)
    pkg["scripts"]["start"] = "npx tsc && node index.js"
    with d.joinpath("package.json").open("w", encoding="utf8") as fid:
        json.dump(pkg, fid, indent=4)
    subprocess.run(
        ["npm", "install", "--save-dev", "typescript"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["npx", "tsc", "--init"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/index.js\n/node_modules\n")


def setup_rs(d: Path, day: int) -> None:
    """Set up the directory as a Rust Crate."""
    subprocess.run(
        ["cargo", "init", "--name", f"day{day:02d}", "--bin", "--vcs", "none"],
        check=True,
        cwd=d,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/target\n")
    with d.joinpath("src", "main.rs").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "fn part1() {}\n",
                "\n",
                "fn part2() {}\n",
                "\n",
                "fn main() {\n",
                "let (p1, p2) = if let Some(which) = std::env::args().nth(1) {\n"
                '        (which == "1", which == "2")\n'
                "    } else {\n"
                "        (true, true)\n"
                "    };\n"
                "    if p1 {\n"
                '        println!("Part 1");\n'
                "        part1();\n"
                "    }\n"
                "    if p2 {\n"
                '        println!("Part 2");\n'
                "        part2();\n"
                "    }\n"
                "}\n",
            ],
        )


SETUPS: dict[Language, Callable[[Path, int], None]] = {
    "go": setup_go,
    "py": setup_py,
    "js": setup_js,
    "ts": setup_ts,
    "rs": setup_rs,
}
"""Setup function mapping. The value is a function that will take in the path
and the current day, and set up the directory given by the path for that
language"""

if __name__ == "__main__":
    args = parse_args()
    p = Path(f"day{args.day:02d}", f"{args.lang}-{args.user}-day{args.day:02d}")
    if p.is_dir():
        print("You've already started on that!", file=sys.stderr)
        sys.exit(1)
    p.mkdir(parents=True, exist_ok=True)
    SETUPS[args.lang](p, args.day)
    subprocess.run(["code", p.resolve()], check=True)

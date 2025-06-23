#!/usr/bin/env python3
"""Set up a new directory for an attempt."""

from __future__ import annotations

import json
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from getpass import getuser
from pathlib import Path
from typing import Callable, Literal

type Language = Literal["rs", "py", "go", "js", "ts"]
"""An allowed programming language suffix"""

SUFFIXES: list[Language] = ["go", "js", "py", "rs", "ts"]
"""All the allowed suffixes"""

LANGS: dict[str, Language] = {
    "rust": "rs",
    "python": "py",
    "go": "go",
    "javascript": "js",
    "typescript": "ts",
}
"""Programming language names mapped to their standardized suffix."""


def parse_args() -> Namespace:
    """Parse CLI Arguments."""
    parser = ArgumentParser()
    langs = set(LANGS.keys()).union(LANGS.values())
    parser.add_argument("day", type=int, help="Day you want to setup, starting with 1")
    parser.add_argument("lang", choices=langs, help="Language you want to use")
    parser.add_argument(
        "user",
        choices=["ahr", "ukr"],
        help="Who are you",
        default="ahr" if getuser().startswith("al") else "ukr",
    )
    return parser.parse_args()


def setup_py(d: Path, day: int) -> None:
    """Set up the directory as a Python3 script."""
    subprocess.run(["python3", "-m", "venv", ".venv"], check=False, cwd=d)
    with d.joinpath("main.py").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "#!/usr/bin/env python3\n",
                f'"""Python implementation for day {day:02d}\n',
                "\n",
                "def part1():\n",
                "    pass\n",
                "\n",
                "\n",
                "def part2():\n",
                "    pass\n",
                "\n",
                'if __name__ == "__main__":\n',
                "    print('Part 1')\n    part1()\n    print('Part 2')\n    part2()\n",
            ],
        )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/.venv\n*.pyc\n__pycache__\n")


def setup_go(d: Path, day: int) -> None:
    """Set up the directory as a go module."""
    subprocess.run(["go", "mod", "init", f"day{day:02d}"], check=False, cwd=d)
    with d.joinpath("main.go").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "package main\n",
                "\n",
                'import "fmt"\n\n',
                "func part1() {}\n",
                "\n",
                "func part2() {}\n",
                "\n",
                "func main() {\n",
                '    fmt.Println("Part 1")\n',
                '    part1()\n    fmt.Println("Part 2")\n',
                "    part2()\n",
                "}\n",
            ],
        )


def setup_js(d: Path, day: int) -> None:
    """Set up the directory as a node.js script."""
    subprocess.run(
        ["npm", "init", "-y", "--silent"],
        check=False,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath("package.json").open("r", encoding="utf8") as fid:
        pkg = json.load(fid)
    pkg["name"] = f"day{day:02d}"
    pkg["scripts"]["start"] = "node index.js"
    with d.joinpath("package.json").open("w", encoding="utf8") as fid:
        json.dump(pkg, fid, indent=4)
    with d.joinpath("index.js").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "function part1() {}\n",
                "\n",
                "function part2() {}\n",
                "\n",
                "console.log('Part 1');\n",
                "part1();\nconsole.log('Part 2');\n",
                "part2();\n",
            ],
        )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/node_modules\n")


def setup_ts(d: Path, day: int) -> None:
    """Set up the directory as a Typescript (to node.js) script."""
    subprocess.run(
        ["npm", "init", "-y"],
        check=False,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath("package.json").open("r", encoding="utf8") as fid:
        pkg = json.load(fid)
    pkg["name"] = f"day{day:02d}"
    pkg["scripts"]["start"] = "npx tsc && node index.js"
    with d.joinpath("package.json").open("w", encoding="utf8") as fid:
        json.dump(pkg, fid, indent=4)
    subprocess.run(
        ["npm", "install", "--save-dev", "typescript"],
        check=False,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    subprocess.run(
        ["npx", "tsc", "--init"],
        check=False,
        cwd=d,
        stdout=subprocess.DEVNULL,
    )
    with d.joinpath("index.ts").open("w", encoding="utf8") as fid:
        fid.writelines(
            [
                "function part1() {}\n",
                "\n",
                "function part2() {}\n",
                "\n",
                "console.log('Part 1');\n",
                "part1();\nconsole.log('Part 2');\n",
                "part2();\n",
            ],
        )
    with d.joinpath(".gitignore").open("w", encoding="utf8") as fid:
        fid.write("/index.js\n/node_modules\n")


def setup_rs(d: Path, day: int) -> None:
    """Set up the directory as a Rust Crate."""
    subprocess.run(
        ["cargo", "init", "--name", f"day{day:02d}", "--bin", "--vcs", "none"],
        check=False,
        cwd=d,
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
                '    println!("Part 1");\n',
                "    part1();\n",
                '    println!("Part 2");\n',
                "    part2();\n",
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
    lang: Language | None = LANGS.get(args.lang, args.lang)
    if args.lang not in SUFFIXES:
        print(f"Unknown language {lang}", file=sys.stderr)
        sys.exit(1)
    p = Path(f"day{args.day:02d}", args.lang, args.user)
    if p.is_dir():
        print("You've already started on that!", file=sys.stderr)
        sys.exit(1)
    p.mkdir(parents=True, exist_ok=True)
    SETUPS[args.lang](p, args.day)
    subprocess.run(["code", p.resolve()], check=False)

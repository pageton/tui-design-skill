#!/usr/bin/env python3
"""Check that ASCII mockups in markdown render at a fixed width.

A mockup is a run of >= 3 consecutive lines inside a fenced code block
where every line both starts and ends with a box-drawing character, and
at least one line in the run contains a horizontal border (3+ border
characters in a row). Directory trees and indented prose are ignored
because their lines do not end with a box-drawing character.

Every line of a run must have the same display width. A misaligned
mockup is worse than no mockup (see AGENTS.md).

Usage: python3 scripts/check-mockups.py [file.md ...]
With no arguments, scans the skill's markdown files.
Exit code 0 = all mockups aligned, 1 = violations found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_PATHS = [
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "commands/*.md",
    "references/*.md",
    "frameworks/*.md",
    "patterns/*.md",
    "projects/*/README.md",
]

BOX_CHARS = set("─│┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬+|-=")
BORDER_RUN = re.compile(r"[─═+-]{3,}")


def is_boxed(line: str) -> bool:
    s = line.strip()
    return len(s) >= 2 and s[0] in BOX_CHARS and s[-1] in BOX_CHARS


def extract_blocks(text: str) -> list[list[tuple[int, str]]]:
    """Return fenced code blocks as lists of (absolute line number, line).

    Follows CommonMark fence rules: a closing fence must be at least as
    long as the opening fence, so ``` inside a ```` block is content.
    """
    blocks: list[list[tuple[int, str]]] = []
    open_len = 0
    buf: list[tuple[int, str]] = []
    for no, line in enumerate(text.split("\n"), start=1):
        m = re.match(r"^(`{3,})(.*)$", line)
        if open_len == 0:
            if m and "`" not in m.group(2):
                open_len = len(m.group(1))
                buf = []
        elif (
            re.match(r"^`{3,}\s*$", line)
            and len(line) - len(line.lstrip("`")) >= open_len
        ):
            blocks.append(buf)
            open_len = 0
        else:
            buf.append((no, line))
    if open_len:
        blocks.append(buf)
    return blocks


def check_file(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")

    def flush(run: list[tuple[int, str]]) -> None:
        if len(run) < 3 or not any(BORDER_RUN.search(l) for _, l in run):
            return
        widths: dict[int, list[int]] = {}
        for line_no, line in run:
            widths.setdefault(len(line.rstrip()), []).append(line_no)
        if len(widths) < 2:
            return
        expected = max(widths, key=lambda w: len(widths[w]))
        problems.append(
            f"{path}:{run[0][0]}  mockup lines {run[0][0]}-{run[-1][0]}: "
            f"expected width {expected}, got "
            + ", ".join(
                f"line {n} = {w}"
                for w in sorted(widths, reverse=True)
                if w != expected
                for n in widths[w]
            )
        )

    for block in extract_blocks(text):
        run: list[tuple[int, str]] = []
        for line_no, line in block:
            if is_boxed(line):
                run.append((line_no, line))
            else:
                flush(run)
                run = []
        flush(run)
    return problems


def main() -> int:
    paths = []
    if len(sys.argv) > 1:
        paths = [Path(a) for a in sys.argv[1:]]
    else:
        for pattern in SCAN_PATHS:
            paths.extend(sorted(ROOT.glob(pattern)))
    problems = [p for path in paths for p in check_file(path)]
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} misaligned mockup(s) in {len(paths)} files checked")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

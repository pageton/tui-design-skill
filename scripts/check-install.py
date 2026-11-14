#!/usr/bin/env python3
"""Verify the documented installation methods actually work.

Two layers:

1. Simulation — extract every ```bash block from README.md, keep only
   the `mkdir`/`cp` lines (git clone, npx, and agent-internal commands
   are skipped), and run them with $HOME pointed at a temp directory
   that symlinks ~/Projects/tui-design-skill to this repo. Then verify
   what landed: every cp source existed, every destination matches the
   repo bytes, each tool got exactly one skills/tui-design directory
   with one SKILL.md, and nothing is nested or duplicated.

2. Doc contracts — the install docs must warn against installing the
   plugin AND the skills pack for the same agent ("not both"), and an
   "Updating" section must cover the skills CLI (`npx skills update`)
   and the plugin marketplace.

Usage: python3 scripts/check-install.py
Exit code 0 = documented installs verified, 1 = problems found.
"""

import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_LINK = "~/Projects/tui-design-skill"
RUNNABLE = {"mkdir", "cp"}


def bash_blocks(text: str) -> list[list[str]]:
    """Return the line lists of all ```bash fenced blocks."""
    blocks: list[list[str]] = []
    buf: list[str] = []
    inside = False
    for line in text.splitlines():
        if not inside and line.startswith("```bash"):
            inside, buf = True, []
        elif inside and line.startswith("```"):
            blocks.append(buf)
            inside = False
        elif inside:
            buf.append(line)
    return blocks


def join_continuations(lines: list[str]) -> list[str]:
    """Merge lines ending in backslash into single commands."""
    merged: list[str] = []
    for line in lines:
        if merged and merged[-1].endswith("\\"):
            merged[-1] = merged[-1][:-1] + line.strip()
        else:
            merged.append(line)
    return merged


def runnable_commands(text: str) -> list[str]:
    commands = []
    for block in bash_blocks(text):
        for line in join_continuations(block):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if shlex.split(stripped)[0] in RUNNABLE:
                commands.append(stripped)
    return commands


def heading_section(text: str, title: str) -> str:
    m = re.search(
        rf"^## {re.escape(title)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.M | re.S
    )
    return m.group(1) if m else ""


def expand_braces(path: str) -> list[str]:
    """Expand a single-level {a,b,c} group; return [path] if none."""
    m = re.search(r"\{([^{}]+)\}", path)
    if not m:
        return [path]
    return [path[: m.start()] + part + path[m.end() :] for part in m.group(1).split(",")]


def resolve(path: str, repo: Path, home: Path) -> Path:
    if path.startswith(REPO_LINK):
        return repo / path[len(REPO_LINK) :].lstrip("/")
    if path.startswith("~/"):
        return home / path[2:]
    return Path(path)


def parse_cp(line: str) -> tuple[list[str], str] | None:
    """Return (sources, dest) for a cp command, or None if not a cp."""
    parts = shlex.split(line)
    if parts[0] != "cp":
        return None
    args = [a for a in parts[1:] if not a.startswith("-")]
    if len(args) < 2:
        return None
    return args[:-1], args[-1]


def walk(path: Path) -> list[Path]:
    """os.walk without following symlinks (the temp HOME links to the repo)."""
    out: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(path, followlinks=False):
        out.extend(Path(dirpath) / f for f in filenames)
    return out


def simulate_install(readme_text: str, repo: Path, home: Path) -> list[str]:
    problems: list[str] = []
    commands = runnable_commands(readme_text)
    cps: list[str] = []

    env = dict(os.environ, HOME=str(home))
    for line in commands:
        proc = subprocess.run(
            ["bash", "-c", line], cwd=home, env=env,
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            problems.append(
                f"README install command failed: {line}\n    {proc.stderr.strip()}"
            )
        if line.split()[0] == "cp":
            cps.append(line)

    # Pre-check sources and verify destinations against repo bytes.
    for line in cps:
        parsed = parse_cp(line)
        if parsed is None:
            continue
        sources, dest = parsed
        dest_path = resolve(dest, repo, home)
        for src in sources:
            for variant in expand_braces(src):
                src_path = resolve(variant, repo, home)
                if not src_path.exists():
                    problems.append(f"README copies {variant}, which does not exist")
                    continue
                target = dest_path / src_path.name if dest_path.is_dir() else dest_path
                if not target.exists():
                    problems.append(f"{line}: {target} was not created")
                elif src_path.is_file() and target.read_bytes() != src_path.read_bytes():
                    problems.append(f"{line}: {target} differs from {variant}")

    # Structural checks: one clean skill directory per tool, no duplicates.
    skill_dirs = {
        p.parent for p in walk(home) if p.name == "SKILL.md"
    }
    if not skill_dirs:
        problems.append("README install commands installed no skills directory")
    for d in sorted(skill_dirs):
        rel = str(d.relative_to(home))
        if not (d / "SKILL.md").is_file():
            problems.append(f"{rel}: SKILL.md missing after install")
        if (d / "tui-design").is_dir():
            problems.append(f"{rel}: nested tui-design/ directory (duplicated install)")
        if (d / "tui-design.md").is_file():
            problems.append(f"{rel}: command file installed inside the skills directory")
    return problems


def check_doc_contracts(readme_text: str) -> list[str]:
    problems: list[str] = []
    install = heading_section(readme_text, "Install")
    if "not both" not in install.lower():
        problems.append(
            "README Install section must warn: install the plugin OR the "
            "skills pack for an agent — not both"
        )
    updating = heading_section(readme_text, "Updating")
    if not updating:
        problems.append("README is missing an '## Updating' section")
    else:
        if "npx skills update" not in updating:
            problems.append("README Updating section must cover `npx skills update`")
        if "marketplace" not in updating.lower():
            problems.append("README Updating section must cover plugin marketplace updates")
    return problems


def check_install(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md: missing"]
    text = readme.read_text(encoding="utf-8")
    problems = check_doc_contracts(text)
    with tempfile.TemporaryDirectory() as td:
        home = Path(td)
        (home / "Projects").mkdir()
        (home / "Projects" / "tui-design-skill").symlink_to(root.resolve())
        problems.extend(simulate_install(text, root, home))
    return problems


def main() -> int:
    problems = check_install(ROOT)
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} installation problem(s) found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

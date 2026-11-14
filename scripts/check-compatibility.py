#!/usr/bin/env python3
"""Keep the skill pack portable across AI coding agents.

The core skill files (SKILL.md, references/, frameworks/, patterns/,
projects/) are loaded verbatim by every supported agent, so they must
stay agent-agnostic: no agent brand names, no harness-specific
invocation syntax ("Skill tool", $ARGUMENTS, /plugin), no hardcoded
install paths. Agent-specific content lives only in the four command
files and in README install docs.

This script enforces that split:

1. Pack cleanliness — scan the skill pack's markdown (excluding
   vendored node_modules) for agent-specific terms.
2. Command portability — the command files must not hardcode install
   paths or repo-relative skill paths; they delegate to the installed
   skill.
3. Compatibility docs — README must carry an "Agent Compatibility"
   section that names the four supported agents.

Usage: python3 scripts/check-compatibility.py
Exit code 0 = pack is portable, 1 = agent-specific content found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "tui-design"
COMMAND_FILES = [
    "commands/tui-design.md",
    "opencode/commands/tui-design.md",
    "codex/commands/tui-design.md",
    "zcode/commands/tui-design.md",
]
AGENTS = ["Claude Code", "OpenCode", "Codex", "ZCode"]

# Patterns that have no business inside the skill pack. Note: "Cursor"
# (the editor) is deliberately NOT banned — "cursor" is core TUI
# vocabulary and appears capitalized at the start of phrases throughout
# the pack; the false positives outweigh the near-zero risk.
PACK_PATTERNS = [
    (re.compile(r"\bclaude\b", re.I), "agent brand name"),
    (re.compile(r"\bcodex\b", re.I), "agent brand name"),
    (re.compile(r"\bopencode\b", re.I), "agent brand name"),
    (re.compile(r"\bzcode\b", re.I), "agent brand name"),
    (re.compile(r"\bwindsurf\b", re.I), "agent brand name"),
    (re.compile(r"\bcopilot\b", re.I), "agent brand name"),
    (re.compile(r"\bgemini\b", re.I), "agent brand name"),
    (re.compile(r"\bskill tool\b", re.I), "harness-specific invocation"),
    (re.compile(r"\$ARGUMENTS"), "command-file substitution"),
    (re.compile(r"/plugin\b"), "harness-specific command"),
    (re.compile(r"slash command", re.I), "harness-specific concept"),
    (re.compile(r"(~|\bhome/)[\w.-]*/\.(claude|codex|config/opencode|zcode)"), "install path"),
]


def pack_markdown(root: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in ["SKILL.md", "references/*.md", "frameworks/*.md",
                    "patterns/*.md", "projects/*.md", "projects/*/*.md"]:
        paths.extend(sorted((root / "skills" / "tui-design").glob(pattern)))
    return [p for p in paths if p.is_file() and "node_modules" not in p.parts]


def check_pack(root: Path) -> list[str]:
    problems: list[str] = []
    for path in pack_markdown(root):
        rel = str(path.relative_to(root))
        for no, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for pattern, label in PACK_PATTERNS:
                m = pattern.search(line)
                if m:
                    problems.append(f"{rel}:{no}: {label}: {m.group(0)!r}")
    return problems


def check_commands(root: Path) -> list[str]:
    problems: list[str] = []
    for rel in COMMAND_FILES:
        path = root / rel
        if not path.is_file():
            problems.append(f"{rel}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "skills/tui-design" in text:
            problems.append(f"{rel}: hardcodes a repo-relative skill path")
        for pattern in (re.compile(r"~/"), re.compile(r"/home/")):
            if pattern.search(text):
                problems.append(f"{rel}: hardcodes an absolute install path")
                break
    return problems


def check_readme(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md: missing"]
    text = readme.read_text(encoding="utf-8")
    m = re.search(r"^## Agent Compatibility[ \t]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return ["README.md: missing an '## Agent Compatibility' section"]
    problems = []
    for agent in AGENTS:
        if agent.lower() not in m.group(1).lower():
            problems.append(f"README.md: Agent Compatibility table omits {agent}")
    return problems


def main() -> int:
    checks = [check_pack, check_commands, check_readme]
    problems = [p for check in checks for p in check(ROOT)]
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} compatibility problem(s) found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

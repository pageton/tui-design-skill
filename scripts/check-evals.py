#!/usr/bin/env python3
"""Validate the skill evaluation scenarios in evals/.

Each scenario file (evals/*.md except README.md) must follow the fixed
skeleton — Category, Prompt, Fixture, Pass Criteria, Fail Signals,
References Expected — with a canonical category, a non-trivial prompt,
enough criteria to grade against, and reference paths that exist in the
skill pack. Every canonical category must be covered by at least one
scenario, so a new category cannot ship without an eval.

Usage: python3 scripts/check-evals.py
Exit code 0 = scenarios valid and coverage complete, 1 = problems found.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS_DIR = ROOT / "evals"
SKILL_DIR = ROOT / "skills" / "tui-design"

REQUIRED_SECTIONS = [
    "Category",
    "Prompt",
    "Fixture",
    "Pass Criteria",
    "Fail Signals",
    "References Expected",
]
CATEGORIES = [
    "new-tui",
    "cli-to-tui",
    "rtl-bidi",
    "unicode",
    "rendering-troubleshooting",
    "framework-selection",
]
MIN_PASS_CRITERIA = 3
MIN_FAIL_SIGNALS = 2
MIN_PROMPT_CHARS = 40
REF_RE = re.compile(r"`((?:references|frameworks|patterns|templates|projects)/[^`]+)`")


def headings(text: str) -> list[str]:
    return re.findall(r"^## (.+?)\s*$", text, re.M)


def section(text: str, title: str) -> str:
    m = re.search(
        rf"^## {re.escape(title)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.M | re.S
    )
    return m.group(1) if m else ""


def bullets(text: str) -> list[str]:
    return re.findall(r"^\s*[-*] +(.+)$", text, re.M)


def check_eval(path: Path, skill_dir: Path) -> tuple[list[str], str | None]:
    """Return (problems, category) for one scenario file."""
    problems: list[str] = []
    rel = str(path.relative_to(path.parent.parent))
    text = path.read_text(encoding="utf-8")

    if not text.startswith("# Eval: "):
        problems.append(f"{rel}: must start with an '# Eval: <title>' heading")

    found = headings(text)
    missing = [s for s in REQUIRED_SECTIONS if s not in found]
    order = [s for s in found if s in REQUIRED_SECTIONS]
    if missing or order != REQUIRED_SECTIONS:
        detail = f"missing {missing}" if missing else f"found order {order}"
        problems.append(
            f"{rel}: section skeleton wrong ({detail}); expected {REQUIRED_SECTIONS}"
        )

    m = re.search(r"^`([a-z-]+)`\s*$", section(text, "Category"), re.M)
    category = m.group(1) if m else None
    if category is None:
        problems.append(f"{rel}: Category must be a single backticked token")
    elif category not in CATEGORIES:
        problems.append(
            f"{rel}: unknown category {category!r}; canonical: {', '.join(CATEGORIES)}"
        )

    prompt = section(text, "Prompt").strip()
    if len(prompt) < MIN_PROMPT_CHARS:
        problems.append(f"{rel}: Prompt too short (<{MIN_PROMPT_CHARS} chars)")

    if not section(text, "Fixture").strip():
        problems.append(f"{rel}: Fixture section is empty")

    criteria = bullets(section(text, "Pass Criteria"))
    if len(criteria) < MIN_PASS_CRITERIA:
        problems.append(
            f"{rel}: only {len(criteria)} pass criteria "
            f"(need >= {MIN_PASS_CRITERIA})"
        )
    signals = bullets(section(text, "Fail Signals"))
    if len(signals) < MIN_FAIL_SIGNALS:
        problems.append(
            f"{rel}: only {len(signals)} fail signals (need >= {MIN_FAIL_SIGNALS})"
        )

    refs = REF_RE.findall(section(text, "References Expected"))
    if not refs:
        problems.append(f"{rel}: References Expected lists no skill paths")
    for ref in refs:
        if not (skill_dir / ref).exists():
            problems.append(f"{rel}: References Expected cites {ref}, which does not exist")
    return problems, category


def check_all(root: Path) -> tuple[list[str], int, int]:
    """Return (problems, scenario count, categories covered)."""
    problems: list[str] = []
    evals_dir = root / "evals"
    skill_dir = root / "skills" / "tui-design"
    if not evals_dir.is_dir():
        return ["evals/: missing"], 0, 0
    if not (evals_dir / "README.md").is_file():
        problems.append("evals/README.md: missing (how to run the scenarios)")

    scenarios = sorted(p for p in evals_dir.glob("*.md") if p.name != "README.md")
    if not scenarios:
        problems.append("evals/: no scenario files found")

    covered: set[str] = set()
    for path in scenarios:
        file_problems, category = check_eval(path, skill_dir)
        problems.extend(file_problems)
        if category:
            covered.add(category)

    for category in CATEGORIES:
        if category not in covered:
            problems.append(f"evals/: category {category!r} has no scenario")
    return problems, len(scenarios), len(covered)


def main() -> int:
    problems, count, covered = check_all(ROOT)
    for problem in problems:
        print(problem)
    print(
        f"\n{len(problems)} eval problem(s) in {count} scenario(s), "
        f"{covered}/{len(CATEGORIES)} categories covered"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

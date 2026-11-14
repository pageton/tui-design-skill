#!/usr/bin/env python3
"""Check that cross-references across the repo stay in sync.

AGENTS.md requires that when a skill file is added, renamed, or
removed, the SKILL.md "Reference Documents" list, the README
"What's Included" tree, the four per-tool command files, and the
plugin manifests are all updated in the same change. This script
verifies those invariants mechanically:

1. Skill identity — SKILL.md frontmatter name matches the skill
   directory, and the description is present, at most 1024
   characters, and trigger-phrased (contains "Use when").
2. Reference Documents — every file under references/, frameworks/,
   and patterns/ is listed in SKILL.md's "Reference Documents"
   section (exactly, or via its parent directory).
3. Mentions — every relative skill path mentioned anywhere in
   SKILL.md (references/…, frameworks/…, patterns/…, templates/…,
   projects/…), and every path listed under "Reference Documents",
   exists on disk.
4. README tree — the "What's Included" tree lists every reference,
   framework, and pattern file, plus SKILL.md, the command files,
   and the validation scripts.
5. Command sync — the four command files (commands/, opencode/
   commands/, codex/commands/, zcode/commands/) are byte-identical
   and pass through $ARGUMENTS.
6. Manifests — plugin.json and marketplace.json parse, every path
   they declare exists, plugin.json's name matches the skill, and
   the marketplace lists the plugin.

Usage: python3 scripts/check-crossrefs.py
Exit code 0 = all cross-references in sync, 1 = drift found.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMAND_FILES = [
    "commands/tui-design.md",
    "opencode/commands/tui-design.md",
    "codex/commands/tui-design.md",
    "zcode/commands/tui-design.md",
]
# Directories whose files must appear in SKILL.md's Reference Documents.
LISTED_DIRS = ["references", "frameworks", "patterns"]
PATH_RE = re.compile(
    r"\b((?:references|frameworks|patterns|templates|projects)/"
    r"[A-Za-z0-9][A-Za-z0-9_.-]*)"
)


def frontmatter(text: str) -> dict[str, str]:
    """Parse simple `key: value` frontmatter delimited by --- lines."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def heading_section(text: str, title: str) -> str:
    """Return the body of a `## title` section, up to the next `##`."""
    m = re.search(
        rf"^## {re.escape(title)}[ \t]*\n(.*?)(?=^## |\Z)", text, re.M | re.S
    )
    return m.group(1) if m else ""


def listed_paths(section_text: str) -> list[str]:
    """Backticked skill-relative paths in a section (files or dirs)."""
    paths = []
    for token in re.findall(r"`([^`]+)`", section_text):
        if re.match(r"^(?:references|frameworks|patterns|templates|projects)/", token):
            if "*" not in token and "?" not in token:
                paths.append(token)
    return paths


def readme_tree_block(text: str) -> list[str]:
    """Return the lines of the first fenced block under a section."""
    block: list[str] = []
    inside = False
    for line in heading_section(text, "What's Included").splitlines():
        if not inside:
            if line.startswith("```"):
                inside = True
        elif line.startswith("```"):
            break
        else:
            block.append(line)
    return block


def tree_names(block: list[str]) -> set[str]:
    """Entry names in a README tree block, minus drawing characters."""
    names = set()
    for line in block:
        name = line.split("#", 1)[0].strip(" │├└─")
        if name:
            names.add(name)
    return names


def load_json(path: Path, problems: list[str], rel: str) -> dict | None:
    if not path.is_file():
        problems.append(f"{rel}: missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        problems.append(f"{rel}: invalid JSON ({err})")
        return None


def check_skill(root: Path) -> list[str]:
    problems: list[str] = []
    skill_md = root / "skills" / "tui-design" / "SKILL.md"
    rel = str(skill_md.relative_to(root))
    if not skill_md.is_file():
        return [f"{rel}: missing"]

    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)

    name = fm.get("name", "")
    if name != skill_md.parent.name:
        problems.append(
            f"{rel}: frontmatter name {name!r} does not match "
            f"skill directory {skill_md.parent.name!r}"
        )

    description = fm.get("description", "")
    if not description:
        problems.append(f"{rel}: frontmatter description is missing")
    else:
        if len(description) > 1024:
            problems.append(f"{rel}: frontmatter description exceeds 1024 characters")
        if "use when" not in description.lower():
            problems.append(
                f"{rel}: frontmatter description lacks trigger phrasing "
                '(expected "Use when …")'
            )

    doc_list = listed_paths(heading_section(text, "Reference Documents"))
    if not doc_list:
        problems.append(f"{rel}: 'Reference Documents' section not found or empty")

    for d in LISTED_DIRS:
        for f in sorted((skill_md.parent / d).glob("*.md")):
            exact = f"{d}/{f.name}"
            if exact not in doc_list and f"{d}/" not in doc_list:
                problems.append(
                    f"{rel}: {exact} exists but is not listed under "
                    "'Reference Documents'"
                )

    mentioned = set(PATH_RE.findall(text)) | set(doc_list)
    for p in sorted(mentioned):
        if not (skill_md.parent / p).exists():
            problems.append(f"{rel}: mentions {p}, which does not exist")
    return problems


def check_readme(root: Path) -> list[str]:
    problems: list[str] = []
    readme = root / "README.md"
    rel = str(readme.relative_to(root))
    if not readme.is_file():
        return [f"{rel}: missing"]

    names = tree_names(readme_tree_block(readme.read_text(encoding="utf-8")))
    if not names:
        return [f"{rel}: 'What's Included' tree not found"]

    required = {
        "SKILL.md",
        "tui-design.md",
        "check-mockups.py",
        "check-crossrefs.py",
        "test_check_crossrefs.py",
        "justfile",
        "plugin.json",
        "marketplace.json",
    }
    skill_dir = root / "skills" / "tui-design"
    for d in LISTED_DIRS:
        required.update(f.name for f in (skill_dir / d).glob("*.md"))
    for name in sorted(required - names):
        problems.append(f"{rel}: 'What's Included' tree is missing {name}")
    return problems


def check_commands(root: Path) -> list[str]:
    problems: list[str] = []
    canonical_rel = COMMAND_FILES[0]
    canonical_path = root / canonical_rel
    if not canonical_path.is_file():
        return [f"{canonical_rel}: missing (canonical command file)"]

    canonical = canonical_path.read_text(encoding="utf-8")
    if "$ARGUMENTS" not in canonical:
        problems.append(f"{canonical_rel}: does not pass through $ARGUMENTS")
    if "tui-design" not in canonical:
        problems.append(f"{canonical_rel}: does not reference the tui-design skill")

    for rel in COMMAND_FILES[1:]:
        path = root / rel
        if not path.is_file():
            problems.append(f"{rel}: missing — every tool needs its command file")
        elif path.read_text(encoding="utf-8") != canonical:
            problems.append(
                f"{rel}: differs from {canonical_rel} — keep the four command "
                "files byte-identical"
            )
    return problems


def check_manifests(root: Path) -> list[str]:
    problems: list[str] = []
    plugin = load_json(
        root / ".claude-plugin" / "plugin.json", problems, ".claude-plugin/plugin.json"
    )
    market = load_json(
        root / ".claude-plugin" / "marketplace.json",
        problems,
        ".claude-plugin/marketplace.json",
    )

    skill_md = root / "skills" / "tui-design" / "SKILL.md"
    fm = frontmatter(skill_md.read_text(encoding="utf-8")) if skill_md.is_file() else {}

    if plugin is not None:
        if plugin.get("name") != fm.get("name"):
            problems.append(
                ".claude-plugin/plugin.json: name "
                f"{plugin.get('name')!r} does not match SKILL.md frontmatter "
                f"name {fm.get('name')!r}"
            )
        skills = plugin.get("skills", [])
        if isinstance(skills, str):
            skills = [skills]
        declared = skills + list(plugin.get("commands", []))
        if not declared:
            problems.append(".claude-plugin/plugin.json: declares no skills or commands")
        for entry in declared:
            if not (root / entry.removeprefix("./")).exists():
                problems.append(
                    f".claude-plugin/plugin.json: declares {entry!r}, "
                    "which does not exist"
                )

    if market is not None:
        plugins = market.get("plugins", [])
        if plugin is not None and plugin.get("name") not in {
            p.get("name") for p in plugins
        }:
            problems.append(
                ".claude-plugin/marketplace.json: does not list the "
                f"{plugin.get('name')!r} plugin"
            )
        for p in plugins:
            source = p.get("source", "")
            if source and not (root / source.removeprefix("./")).exists():
                problems.append(
                    f".claude-plugin/marketplace.json: plugin {p.get('name')!r} "
                    f"source {source!r} does not exist"
                )
    return problems


def main() -> int:
    checks = [check_skill, check_readme, check_commands, check_manifests]
    problems = [p for check in checks for p in check(ROOT)]
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} cross-reference problem(s) found")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

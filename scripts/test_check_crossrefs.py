"""Unit tests for check-crossrefs.py.

Each test builds a minimal valid repo in a temp directory, mutates
one thing, and asserts the corresponding check reports it. Run with:

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

# The script uses a hyphenated filename (like check-mockups.py), so it
# cannot be imported by name; load it from its path instead.
_spec = importlib.util.spec_from_file_location(
    "check_crossrefs", Path(__file__).resolve().parent / "check-crossrefs.py"
)
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

SKILL_MD = """---
name: tui-design
description: Design TUIs. Use when the user wants to build or polish a terminal UI.
---

# TUI Design Skill

Body mentions `references/alpha.md` and `frameworks/*.md` (a glob).

## Reference Documents

- `references/alpha.md` — First
- `references/beta.md` — Second
- `frameworks/` — Framework guides
- `patterns/` — Screen patterns
- `projects/` — Example apps
"""

README = (
    "# TUI Design Skill\n"
    "\n"
    "## What's Included\n"
    "\n"
    "```\n"
    "repo/\n"
    "├── .claude-plugin/\n"
    "│   ├── plugin.json\n"
    "│   └── marketplace.json\n"
    "├── commands/\n"
    "│   └── tui-design.md\n"
    "├── opencode/\n"
    "│   └── commands/\n"
    "│       └── tui-design.md\n"
    "├── codex/\n"
    "│   └── commands/\n"
    "│       └── tui-design.md\n"
    "├── zcode/\n"
    "│   └── commands/\n"
    "│       └── tui-design.md\n"
    "├── skills/\n"
    "│   └── tui-design/\n"
    "│       ├── SKILL.md\n"
    "│       ├── references/\n"
    "│       │   ├── alpha.md\n"
    "│       │   └── beta.md\n"
    "│       ├── frameworks/\n"
    "│       │   └── fw.md\n"
    "│       └── patterns/\n"
    "│           └── pat.md\n"
    "├── scripts/\n"
    "│   ├── check-mockups.py\n"
    "│   ├── check-crossrefs.py\n"
    "│   └── test_check_crossrefs.py\n"
    "└── justfile\n"
    "```\n"
)

COMMAND = (
    "---\n"
    "description: Test command\n"
    "---\n"
    "\n"
    "Use the `tui-design` skill.\n"
    "\n"
    "Target: $ARGUMENTS\n"
)

PLUGIN = {
    "name": "tui-design",
    "skills": "./skills/",
    "commands": ["./commands/tui-design.md"],
}

MARKETPLACE = {
    "name": "tui-design-skill",
    "plugins": [{"name": "tui-design", "source": "./"}],
}


class RepoTestCase(unittest.TestCase):
    """Builds a valid minimal repo; each test breaks exactly one thing."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        skill = self.skill_dir()
        for name in ("references", "frameworks", "patterns", "projects"):
            (skill / name).mkdir(parents=True)
        (skill / "references" / "alpha.md").write_text("alpha\n")
        (skill / "references" / "beta.md").write_text("beta\n")
        (skill / "frameworks" / "fw.md").write_text("fw\n")
        (skill / "patterns" / "pat.md").write_text("pat\n")
        (skill / "SKILL.md").write_text(SKILL_MD)
        (self.root / "README.md").write_text(README)
        for rel in cc.COMMAND_FILES:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(COMMAND)
        plugin_dir = self.root / ".claude-plugin"
        plugin_dir.mkdir()
        (plugin_dir / "plugin.json").write_text(json.dumps(PLUGIN))
        (plugin_dir / "marketplace.json").write_text(json.dumps(MARKETPLACE))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def skill_dir(self) -> Path:
        return self.root / "skills" / "tui-design"

    def skill_md(self) -> Path:
        return self.skill_dir() / "SKILL.md"

    def rewrite_skill(self, old: str, new: str) -> None:
        self.skill_md().write_text(
            self.skill_md().read_text().replace(old, new)
        )


class CheckSkillTests(RepoTestCase):
    def test_valid_repo_passes(self) -> None:
        for check in (cc.check_skill, cc.check_readme, cc.check_commands,
                      cc.check_manifests):
            self.assertEqual(check(self.root), [])

    def test_unlisted_pack_file(self) -> None:
        self.rewrite_skill("- `references/beta.md` — Second\n", "")
        self.assertTrue(
            any("references/beta.md" in p for p in cc.check_skill(self.root))
        )

    def test_missing_mentioned_path(self) -> None:
        self.rewrite_skill("references/alpha.md", "references/gamma.md")
        self.assertTrue(
            any("gamma.md" in p for p in cc.check_skill(self.root))
        )

    def test_description_without_triggers(self) -> None:
        self.rewrite_skill(
            "description: Design TUIs. Use when the user wants to build or "
            "polish a terminal UI.",
            "description: Design TUIs.",
        )
        self.assertTrue(
            any("trigger phrasing" in p for p in cc.check_skill(self.root))
        )

    def test_description_too_long(self) -> None:
        self.rewrite_skill(
            "description: Design TUIs. Use when the user wants to build or "
            "polish a terminal UI.",
            "description: " + "x" * 1100,
        )
        self.assertTrue(
            any("1024 characters" in p for p in cc.check_skill(self.root))
        )

    def test_name_mismatch(self) -> None:
        self.rewrite_skill("name: tui-design", "name: other-name")
        self.assertTrue(
            any("does not match" in p for p in cc.check_skill(self.root))
        )


class CheckReadmeTests(RepoTestCase):
    def test_missing_tree_entry(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(
            readme.read_text().replace("│       │   └── beta.md\n", "")
        )
        self.assertTrue(
            any("beta.md" in p for p in cc.check_readme(self.root))
        )

    def test_missing_tree(self) -> None:
        (self.root / "README.md").write_text("# TUI Design Skill\n")
        self.assertTrue(
            any("tree not found" in p for p in cc.check_readme(self.root))
        )


class CheckCommandsTests(RepoTestCase):
    def test_command_drift(self) -> None:
        path = self.root / cc.COMMAND_FILES[1]
        path.write_text(path.read_text() + "extra line\n")
        problems = cc.check_commands(self.root)
        self.assertTrue(any("byte-identical" in p for p in problems))
        self.assertEqual(len(problems), 1)

    def test_missing_command_file(self) -> None:
        (self.root / cc.COMMAND_FILES[3]).unlink()
        problems = cc.check_commands(self.root)
        self.assertTrue(any("every tool needs its command file" in p
                            for p in problems))
        self.assertEqual(len(problems), 1)

    def test_command_without_arguments(self) -> None:
        for rel in cc.COMMAND_FILES:
            (self.root / rel).write_text(COMMAND.replace("$ARGUMENTS", "args"))
        self.assertTrue(
            any("$ARGUMENTS" in p for p in cc.check_commands(self.root))
        )


class CheckManifestsTests(RepoTestCase):
    def test_invalid_plugin_json(self) -> None:
        (self.root / ".claude-plugin" / "plugin.json").write_text("{")
        self.assertTrue(
            any("invalid JSON" in p for p in cc.check_manifests(self.root))
        )

    def test_plugin_declares_missing_path(self) -> None:
        plugin = dict(PLUGIN, commands=["./commands/nope.md"])
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(plugin)
        )
        self.assertTrue(
            any("nope.md" in p for p in cc.check_manifests(self.root))
        )

    def test_plugin_name_mismatch(self) -> None:
        plugin = dict(PLUGIN, name="other-design")
        (self.root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(plugin)
        )
        self.assertTrue(
            any("does not match SKILL.md" in p
                for p in cc.check_manifests(self.root))
        )

    def test_marketplace_missing_plugin(self) -> None:
        marketplace = dict(MARKETPLACE, plugins=[])
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps(marketplace)
        )
        self.assertTrue(
            any("does not list the" in p
                for p in cc.check_manifests(self.root))
        )


if __name__ == "__main__":
    unittest.main()

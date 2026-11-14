"""Unit tests for check-compatibility.py. Run with:

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_compatibility",
    Path(__file__).resolve().parent / "check-compatibility.py",
)
ck = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ck)

COMMAND = "---\ndescription: Test\n---\n\nUse the `tui-design` skill.\n\nTarget: $ARGUMENTS\n"

COMPAT_README = """# TUI Design Skill

## Agent Compatibility

| Agent | Install | Auto-trigger |
|---|---|---|
| Claude Code | plugin | yes |
| OpenCode | skills pack | yes |
| Codex | skills pack | yes |
| ZCode | skills pack | yes |
"""


class CompatTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        skill = self.root / "skills" / "tui-design"
        for d in ("references", "frameworks", "patterns", "projects/app"):
            (skill / d).mkdir(parents=True)
        (skill / "SKILL.md").write_text("# Skill\n\nDesign TUIs.\n")
        (skill / "references" / "r.md").write_text("ref: cursor position\n")
        (skill / "frameworks" / "f.md").write_text("guide\n")
        (skill / "patterns" / "p.md").write_text("pattern\n")
        (skill / "projects" / "app" / "README.md").write_text("app\n")
        for rel in ck.COMMAND_FILES:
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(COMMAND)
        (self.root / "README.md").write_text(COMPAT_README)

    def tearDown(self) -> None:
        self._tmp.cleanup()


class PackTests(CompatTestCase):
    def test_valid_pack_passes(self) -> None:
        for check in (ck.check_pack, ck.check_commands, ck.check_readme):
            self.assertEqual(check(self.root), [])

    def test_terminal_cursor_is_allowed(self) -> None:
        # "cursor" is TUI vocabulary and must not trip the brand-name scan.
        self.assertEqual(ck.check_pack(self.root), [])

    def test_agent_name_in_pack(self) -> None:
        path = self.root / "skills" / "tui-design" / "references" / "r.md"
        path.write_text("Works great with Claude Code.\n")
        self.assertTrue(any("brand name" in p for p in ck.check_pack(self.root)))

    def test_command_syntax_in_pack(self) -> None:
        path = self.root / "skills" / "tui-design" / "SKILL.md"
        path.write_text("Call $ARGUMENTS from the Skill tool.\n")
        problems = ck.check_pack(self.root)
        self.assertTrue(any("$ARGUMENTS" in p for p in problems))
        self.assertTrue(any("Skill tool" in p for p in problems))

    def test_install_path_in_pack(self) -> None:
        path = self.root / "skills" / "tui-design" / "frameworks" / "f.md"
        path.write_text("Copy me to ~/.claude/skills first.\n")
        self.assertTrue(any("install path" in p for p in ck.check_pack(self.root)))


class CommandTests(CompatTestCase):
    def test_command_hardcodes_absolute_path(self) -> None:
        path = self.root / ck.COMMAND_FILES[0]
        path.write_text("Copy from ~/Projects/tui-design-skill.\n")
        self.assertTrue(
            any("absolute install path" in p for p in ck.check_commands(self.root))
        )

    def test_command_hardcodes_repo_path(self) -> None:
        path = self.root / ck.COMMAND_FILES[0]
        path.write_text("Read skills/tui-design/SKILL.md.\n")
        self.assertTrue(
            any("repo-relative" in p for p in ck.check_commands(self.root))
        )


class ReadmeTests(CompatTestCase):
    def test_missing_compat_section(self) -> None:
        (self.root / "README.md").write_text("# TUI Design Skill\n")
        self.assertTrue(
            any("Agent Compatibility" in p for p in ck.check_readme(self.root))
        )

    def test_compat_section_omits_agent(self) -> None:
        readme = self.root / "README.md"
        readme.write_text(readme.read_text().replace("| ZCode | skills pack | yes |", ""))
        self.assertTrue(any("ZCode" in p for p in ck.check_readme(self.root)))


if __name__ == "__main__":
    unittest.main()

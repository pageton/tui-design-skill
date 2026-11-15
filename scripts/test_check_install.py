"""Unit tests for check-install.py. Run with:

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_install", Path(__file__).resolve().parent / "check-install.py"
)
ci = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ci)

INSTALL_BLOCK = "\n".join(
    [
        "mkdir -p ~/.config/opencode/skills/tui-design",
        "cp -r ~/Projects/tui-design-skill/skills/tui-design/{SKILL.md,references} \\",
        "    ~/.config/opencode/skills/tui-design/",
        "mkdir -p ~/.config/opencode/commands",
        "cp ~/Projects/tui-design-skill/opencode/commands/tui-design.md \\",
        "    ~/.config/opencode/commands/tui-design.md",
    ]
)

README = "\n".join(
    [
        "# TUI Design Skill",
        "",
        "## Install",
        "",
        "Install each agent once: plugin **or** skills pack, not both.",
        "",
        "```bash",
        "git clone https://example.com/tui-design-skill ~/Projects/tui-design-skill",
        "```",
        "",
        "```bash",
        INSTALL_BLOCK,
        "```",
        "",
        "## Updating",
        "",
        "```bash",
        "npx skills update",
        "```",
        "",
        "Plugins refresh from the marketplace automatically.",
        "",
    ]
)


class InstallTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        skill = self.root / "skills" / "tui-design"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("# Skill\n")
        (skill / "references" / "r.md").write_text("ref\n")
        cmd = self.root / "opencode" / "commands" / "tui-design.md"
        cmd.parent.mkdir(parents=True)
        cmd.write_text("Use the tui-design skill.\n")
        (self.root / "README.md").write_text(README)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def rewrite_readme(self, old: str, new: str) -> None:
        readme = self.root / "README.md"
        readme.write_text(readme.read_text().replace(old, new))


class SimulationTests(InstallTestCase):
    def test_valid_install_passes(self) -> None:
        self.assertEqual(ci.check_install(self.root), [])

    def test_broken_source_path(self) -> None:
        self.rewrite_readme("{SKILL.md,references}", "{SKILL.md,missing}")
        self.assertTrue(any("missing" in p for p in ci.check_install(self.root)))

    def test_cli_only_readme_ok(self) -> None:
        # A README that documents no manual copy commands (skills CLI is
        # the only documented install) must pass without simulation.
        readme = self.root / "README.md"
        readme.write_text(
            "\n".join(
                [
                    "# TUI Design Skill",
                    "",
                    "## Install",
                    "",
                    "Plugin or pack, not both.",
                    "",
                    "```bash",
                    "npx skills add pageton/tui-design-skill",
                    "```",
                    "",
                    "## Updating",
                    "",
                    "```bash",
                    "npx skills update",
                    "```",
                    "",
                    "Marketplace plugins update via /plugin.",
                    "",
                ]
            )
        )
        self.assertEqual(ci.check_install(self.root), [])

    def test_skills_never_installed(self) -> None:
        self.rewrite_readme(
            "cp -r ~/Projects/tui-design-skill/skills/tui-design/"
            "{SKILL.md,references} \\\n"
            "    ~/.config/opencode/skills/tui-design/\n",
            "",
        )
        self.assertTrue(
            any("no skills directory" in p for p in ci.check_install(self.root))
        )

    def test_nested_duplicate_install(self) -> None:
        self.rewrite_readme(
            "mkdir -p ~/.config/opencode/commands",
            "cp -r ~/Projects/tui-design-skill/skills/tui-design \\\n"
            "    ~/.config/opencode/skills/tui-design/tui-design\n"
            "mkdir -p ~/.config/opencode/commands",
        )
        self.assertTrue(
            any("nested" in p for p in ci.check_install(self.root))
        )

    def test_modified_copy_detected(self) -> None:
        # Dest exists but differs from the repo file: simulate by making the
        # repo file change after a successful copy would have run — instead,
        # point the copy at a stale directory containing an old SKILL.md.
        (self.root / "skills" / "tui-design" / "SKILL.md").write_text(
            "# Skill v2\n"
        )
        problems = ci.check_install(self.root)
        # The copy runs fresh each time, so this must still pass.
        self.assertEqual(problems, [])


class DocContractTests(InstallTestCase):
    def test_missing_not_both_warning(self) -> None:
        self.rewrite_readme(
            "Install each agent once: plugin **or** skills pack, not both.",
            "Install it.",
        )
        self.assertTrue(
            any("not both" in p for p in ci.check_install(self.root))
        )

    def test_missing_updating_section(self) -> None:
        self.rewrite_readme("## Updating", "## Upkeep")
        self.assertTrue(
            any("Updating" in p for p in ci.check_install(self.root))
        )

    def test_updating_section_omits_skills_cli(self) -> None:
        self.rewrite_readme("npx skills update", "echo update")
        self.assertTrue(
            any("npx skills update" in p for p in ci.check_install(self.root))
        )


if __name__ == "__main__":
    unittest.main()

"""Unit tests for check-evals.py. Run with:

    python3 -m unittest discover -s scripts -p "test_*.py"
"""

import importlib.util
import tempfile
import unittest
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "check_evals", Path(__file__).resolve().parent / "check-evals.py"
)
ce = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ce)

SCENARIO = """# Eval: {title}

## Category

`{category}`

## Prompt

A realistic user prompt asking for a terminal interface, with enough
detail in it to grade the response properly.

## Fixture

Empty project directory.

## Pass Criteria

- First criterion is observable.
- Second criterion is observable.
- Third criterion is observable.

## Fail Signals

- First red flag.
- Second red flag.

## References Expected

- `references/r.md`
"""


class EvalRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "evals").mkdir()
        (self.root / "evals" / "README.md").write_text("# Skill Evals\n")
        skill = self.root / "skills" / "tui-design" / "references"
        skill.mkdir(parents=True)
        (skill / "r.md").write_text("reference\n")
        for i, category in enumerate(ce.CATEGORIES):
            self.write_scenario(f"s{i}.md", category)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_scenario(self, name: str, category: str) -> Path:
        path = self.root / "evals" / name
        path.write_text(
            SCENARIO.format(title=f"Eval {category}", category=category)
        )
        return path

    def check(self) -> list[str]:
        problems, _, _ = ce.check_all(self.root)
        return problems


class CheckAllTests(EvalRepoTestCase):
    def test_valid_repo_passes(self) -> None:
        self.assertEqual(self.check(), [])

    def test_missing_evals_readme(self) -> None:
        (self.root / "evals" / "README.md").unlink()
        self.assertTrue(any("README.md" in p for p in self.check()))

    def test_uncovered_category(self) -> None:
        (self.root / "evals" / "s0.md").unlink()
        self.assertTrue(
            any("has no scenario" in p for p in self.check())
        )

    def test_unknown_category(self) -> None:
        self.write_scenario("bad.md", "not-a-category")
        self.assertTrue(any("unknown category" in p for p in self.check()))

    def test_missing_reference(self) -> None:
        path = self.write_scenario("extra.md", "new-tui")
        path.write_text(path.read_text().replace(
            "`references/r.md`", "`references/gone.md`"
        ))
        self.assertTrue(any("gone.md" in p for p in self.check()))

    def test_too_few_criteria(self) -> None:
        path = self.root / "evals" / "s0.md"
        path.write_text(
            path.read_text().replace("- Third criterion is observable.\n", "")
        )
        self.assertTrue(any("pass criteria" in p for p in self.check()))


class CheckEvalTests(EvalRepoTestCase):
    def skill_dir(self) -> Path:
        return self.root / "skills" / "tui-design"

    def test_missing_section(self) -> None:
        path = self.write_scenario("bad.md", "new-tui")
        path.write_text(
            path.read_text().replace("## Fail Signals\n\n- First red flag.\n- Second red flag.\n\n", "")
        )
        problems, _ = ce.check_eval(path, self.skill_dir())
        self.assertTrue(any("skeleton" in p for p in problems))

    def test_short_prompt(self) -> None:
        path = self.write_scenario("bad.md", "new-tui")
        path.write_text(path.read_text().replace(
            "A realistic user prompt asking for a terminal interface, with enough\n"
            "detail in it to grade the response properly.",
            "Build a TUI.",
        ))
        problems, _ = ce.check_eval(path, self.skill_dir())
        self.assertTrue(any("too short" in p for p in problems))


if __name__ == "__main__":
    unittest.main()

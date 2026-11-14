# Skill Evals

Realistic scenarios for evaluating whether the `tui-design` skill produces
good output — not just whether the repo's files are valid. Each scenario is a
prompt a user could plausibly send, a fixture (the state of the project
beforehand), and a grading rubric.

## Categories

| Category | What it exercises |
|---|---|
| `new-tui` | Greenfield TUI generation: design first, architecture, states, tests |
| `cli-to-tui` | Conversion that preserves non-interactive behavior |
| `rtl-bidi` | Arabic/RTL: logical order, alignment-only, emulator dependency |
| `unicode` | Display-width math, grapheme boundaries, regression tests |
| `rendering-troubleshooting` | Layer-by-layer diagnosis, capability detection, terminal restore |
| `framework-selection` | Requirement-driven decision, not a popularity ranking |

Every category must have at least one scenario — `just check-evals` enforces
this, the required section skeleton, and that referenced skill documents
exist.

## Running an eval

1. Install the skill for the agent under test (see `README.md`).
2. Create an empty scratch directory and set up the scenario's **Fixture**
   (copy in the files it shows, or create the state it describes).
3. Start a fresh session and send the scenario's **Prompt** verbatim. Do not
   coach the agent beyond the prompt.
4. Grade the result against **Pass Criteria** (each criterion: pass,
   partial, or fail) and note any **Fail Signals** observed.
5. Record the run in the table below.

A scenario passes only when every pass criterion is pass or partial and no
fail signal fires. If the skill fails a scenario, fix the skill (references,
SKILL.md guidance) — not the scenario — unless the scenario itself is wrong.

## Results

| Date | Agent | Scenario | Result | Notes |
|---|---|---|---|---|
| | | | | |

Run artifacts (responses, verdict JSON) live outside the repo in scratch
directories; re-run by following "Running an eval" above.

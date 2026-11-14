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

Score = pass criteria points (pass 1, partial 0.5, fail 0). Strict pass = no
fail verdicts and no fail signals fired. Baseline arm = same model, same
prompt, skill not loaded; the delta is the skill's contribution.

Run 1 (2026-11-14, GLM-5.3 subagents, blind grading): **with skill 95.3%
(30.5/32), baseline 85.9% (27.5/32), delta +9.4pp**. Zero fail signals in
either arm. Largest skill effects: framework selection (baseline omitted the
no-BiDi note and any terminal contract), CLI conversion (baseline silently
dropped `--version` and wrote no README), and RTL (baseline didn't state that
no framework does BiDi). No effect on greenfield generation and table
alignment — strong-model ceiling. Shared gap in both arms (rendering
troubleshooting): no 256-color tier between truecolor and 16, `TMUX`/
`TERM_PROGRAM` unchecked, cursor-show missing from restore — candidates for
reference updates.

| Date | Agent | Scenario | Result | Notes |
|---|---|---|---|---|
| 2026-11-14 | GLM-5.3 + skill | new-tui-app | 7/7 (100%), strict pass | aligned mockups, Cmd-based polling, all states, 39 tests |
| 2026-11-14 | GLM-5.3 baseline | new-tui-app | 7/7 (100%), strict pass | ceiling effect; skill added nothing measurable here |
| 2026-11-14 | GLM-5.3 + skill | cli-to-tui | 5/5 (100%), strict pass | CLI contract pinned byte-for-byte; README documents the boundary |
| 2026-11-14 | GLM-5.3 baseline | cli-to-tui | 4/5 (80%) | dropped `--version` silently; no README file |
| 2026-11-14 | GLM-5.3 + skill | rtl-arabic | 5/5 (100%), strict pass | reversal removed, all five BiDi emulators named, 21 tests |
| 2026-11-14 | GLM-5.3 baseline | rtl-arabic | 4.5/5 (90%) | never states no framework does BiDi; omitted Ghostty |
| 2026-11-14 | GLM-5.3 + skill | unicode-width | 5/5 (100%), strict pass | whole-file width math, golden render test |
| 2026-11-14 | GLM-5.3 baseline | unicode-width | 5/5 (100%), strict pass | ceiling effect |
| 2026-11-14 | GLM-5.3 + skill | rendering-bug | 4/5 (80%) | partials: no 256-color tier, no TERM_PROGRAM/TMUX check, cursor-show missing from restore |
| 2026-11-14 | GLM-5.3 baseline | rendering-bug | 4/5 (80%) | partials: no 256 tier, no drop accounting, unbounded channel |
| 2026-11-14 | GLM-5.3 + skill | framework-selection | 4.5/5 (90%) | decisive, runner-up + limitations, BiDi note, terminal contract |
| 2026-11-14 | GLM-5.3 baseline | framework-selection | 3/5 (60%), strict fail | no BiDi mention, no terminal contract, no winner limitations |

Run artifacts (responses, verdict JSON) live outside the repo in scratch
directories; re-run by following "Running an eval" above.

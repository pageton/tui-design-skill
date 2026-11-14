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

Run 2 (2026-11-14, same model, blind grading, after the terminal-compatibility
fixes — color tier ladder, ordered restore checklist with cursor-show,
`TERM_PROGRAM`/`TMUX` semantics in `terminal-compatibility.md`, Ratatui guide
and `log-monitor-rust` example synced): **93.8% (30.0/32), zero fail
signals, zero fail verdicts**. Of the three run-1 rendering-troubleshooting
gaps: 256-color tier — **fixed** (grader verified a truecolor → `Indexed` →
ANSI → mono ladder with no hardcoded truecolor); cursor restore — **fixed**
(idempotent ordered checklist incl. `Show` on panic/error/normal paths);
`TERM_PROGRAM`/`TMUX` — **partially fixed** (color tier detection now works
via `TERM`, but the two vars are still not consulted directly). The
remaining partials (no README file in cli-to-tui, one-sided
unicode/testability axes in framework-selection) sit on criteria the
reference changes did not touch — single-run variance, not regressions.

| Date | Agent | Scenario | Result | Notes |
|---|---|---|---|---|
| 2026-11-14 | GLM-5.3 + skill (run 2) | new-tui-app | 7/7 (100%), strict pass | 50 tests incl. fixed-dimension frames; minor overclaim noted (PTY smoke test) |
| 2026-11-14 | GLM-5.3 + skill (run 2) | cli-to-tui | 4.5/5 (90%) | boundary documented in response + module docstring, but no README file this run |
| 2026-11-14 | GLM-5.3 + skill (run 2) | rtl-arabic | 5/5 (100%), strict pass | 22 tests green; BiDi rationale and emulator list complete |
| 2026-11-14 | GLM-5.3 + skill (run 2) | unicode-width | 5/5 (100%), strict pass | whole-file width math; deps pinned to ratatui's existing tree |
| 2026-11-14 | GLM-5.3 + skill (run 2) | rendering-bug | 4.5/5 (90%) | 256-tier + cursor restore fixed; partial: `TMUX`/`TERM_PROGRAM` still unconsulted |
| 2026-11-14 | GLM-5.3 + skill (run 2) | framework-selection | 4/5 (80%) | decisive + runner-up + limitations; partials: unicode/testability axes one-sided, BiDi framed as a Ratatui-only cost |

Run 3 (2026-11-14, same model, blind grading, after fixing the three run-2
gaps — direct `TMUX`/`TERM_PROGRAM` consultation, README-as-file
deliverable, all-axes framework comparison): **96.9% (31.0/32), zero fail
signals, zero fail verdicts**. All three gaps verified fixed by graders
reading the generated code: rendering-bug capability detection now reads
`NO_COLOR`/`COLORTERM`/`TERM`/`TMUX`/`TERM_PROGRAM` with a truecolor → 256
→ 16 → mono ladder; cli-to-tui shipped a real `README.md` documenting the
CLI/TUI boundary (as did new-tui-app and rendering-bug); framework
selection compared every candidate on rendering, terminal/tmux, Unicode,
and testability. New, smaller residuals this run: rendering-bug restores
on panic and normal exit but lacks an RAII guard for `?`-propagated errors
and traps no signals; framework selection states no explicit minimum
terminal contract.

| Date | Agent | Scenario | Result | Notes |
|---|---|---|---|---|
| 2026-11-14 | GLM-5.3 + skill (run 3) | new-tui-app | 7/7 (100%), strict pass | 40 tests, exact-width mockups verified programmatically |
| 2026-11-14 | GLM-5.3 + skill (run 3) | cli-to-tui | 5/5 (100%), strict pass | README.md on disk; CI contract byte-pinned (41+11 tests) |
| 2026-11-14 | GLM-5.3 + skill (run 3) | rtl-arabic | 5/5 (100%), strict pass | reversal gone; grapheme-snapped highlighting; 12 tests |
| 2026-11-14 | GLM-5.3 + skill (run 3) | unicode-width | 5/5 (100%), strict pass | whole-file width math; 9 tests; deps = ratatui's tree |
| 2026-11-14 | GLM-5.3 + skill (run 3) | rendering-bug | 4.5/5 (90%) | partial: no RAII guard for `?` error paths; SIGTERM untrapped |
| 2026-11-14 | GLM-5.3 + skill (run 3) | framework-selection | 4.5/5 (90%) | partial: no explicit minimum terminal contract stated |

Run 4 — cross-model (2026-11-14): the same six scenarios, prompts, fixtures,
and rubrics run through **Codex CLI 0.157.1 (model `gpt-6-luna`)** with the
skill supplied at the same path. Graders were blind to the arm and weighed
the project files as primary evidence (Codex exec mode writes terse
summaries and edits code in place). Result: **81.2% (26.0/32), 3 fail
signals, 3 fail verdicts — all in the tests/completeness class** (no tests
shipped in new-tui-app/unicode-width/rtl-arabic, no truncation in
unicode-width, a frameless misaligned mockup in new-tui-app).

The important signal for the skill: **every fix from this session
transferred to the second model.** Codex's capability detection "consults
TMUX/TERM_PROGRAM and distrusts TERM alone" with the full color-tier
ladder (rendering-bug criterion 2 pass); it shipped a README.md documenting
the CLI/TUI boundary (cli-to-tui 5/5); and its framework memo compared all
candidates on rendering, SSH/tmux, Unicode/BiDi, and testability with a
stated minimum terminal contract (framework-selection 5/5). Concept-level
fail signals stayed at zero — no text reversal, no BiDi overclaims, no
duplicate width libraries.

| Date | Agent | Scenario | Result | Notes |
|---|---|---|---|---|
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | new-tui-app | 5.5/7 (79%) | fail: no tests (admitted); mockup frameless with 1-col misalignments |
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | cli-to-tui | 5/5 (100%), strict pass | README.md on disk; TUI opt-in; piped behavior verified |
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | rtl-arabic | 3.5/5 (70%) | reversal gone, logical order kept; no tests, no right-alignment wiring |
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | unicode-width | 2.5/5 (50%) | width crate used, but per-char not clusters; no truncation, no tests |
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | rendering-bug | 4.5/5 (90%) | TMUX/TERM_PROGRAM ladder present; bounded batches, 50ms resize debounce |
| 2026-11-14 | gpt-6-luna + skill (Codex CLI) | framework-selection | 5/5 (100%), strict pass | all four axes + runner-up + limits + minimum terminal contract |

Remaining known limitations (runs 3-4): error-path terminal restore and
signal trapping in generated code; minimum-terminal-contract statements in
selection memos; completion-class rubric items (tests, README files) depend
on the model's execution depth — Codex in exec mode ships minimal diffs, so
tests and truncation were skipped there; single-run arms carry roughly
±0.5 criterion of noise, so treat sub-point deltas as variance unless the
verdict changes.

Run artifacts (responses, verdict JSON) live outside the repo in scratch
directories; re-run by following "Running an eval" above.

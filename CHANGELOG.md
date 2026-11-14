# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[SemVer](https://semver.org/).

## [0.2.0] — 2026-11-14

### Added

- Automated cross-reference validation (`just check-crossrefs`): SKILL.md
  Reference Documents ↔ pack files ↔ README tree ↔ byte-identical command
  files ↔ plugin manifests; unit-tested.
- Skill evaluation framework (`evals/`): six graded scenarios (new TUI,
  CLI-to-TUI conversion, RTL/Arabic, Unicode width, rendering
  troubleshooting, framework selection) with fixtures and rubrics;
  `just check-evals` enforces skeleton, category coverage, and reference
  validity.
- Installation verification (`just check-install`): executes the README's
  documented manual-install commands against a temp `$HOME`, verifies
  destinations and byte equality, rejects duplicated/nested installs, and
  enforces Updating docs plus the plugin-or-pack "not both" warning.
- Agent-compatibility enforcement (`just check-compatibility`): the skill
  pack stays agent-agnostic (no agent brands, harness syntax, or install
  paths); command files stay portable; README carries a compatibility
  matrix.
- Color tier ladder in `terminal-compatibility.md`: NO_COLOR → mono,
  truecolor (COLORTERM / `-direct`), 256 (`TERM` contains `256color`),
  16 — with `TMUX`/`TERM_PROGRAM` consulted directly and the
  inside-tmux COLORTERM-forwarding rule.
- `ColorTier` detection module in the `log-monitor-rust` example (10 unit
  tests) implementing the ladder; project test count 14 → 24.
- CHANGELOG.md; README sections: Updating, Agent Compatibility,
  validation-pipeline reference.

### Changed

- SKILL.md frontmatter description rewritten as explicit trigger
  conditions (quoted keywords, framework names) for reliable
  auto-invocation.
- Terminal restore is now an ordered, idempotent checklist everywhere
  (leave alt screen → show cursor → disable raw mode → disable mouse/paste
  → flush); the Ratatui guide example and `log-monitor-rust` follow it.
- Framework selection now requires comparing every serious candidate on
  every relevant axis (rendering at the project's update frequency,
  terminal/tmux compatibility, Unicode width, BiDi, testability).
- Generated TUIs must ship a `README.md` file on disk (Workflows 1 and 2,
  Output Standards) — not documentation embedded only in the reply.
- The four per-tool command files are byte-identical thin wrappers.

### Verified

- Evaluation runs (blind rubric grading, `evals/README.md` has the full
  tables): run 1 with-skill 95.3% vs baseline 85.9% (+9.4pp); run 2 fixed
  the 256-color tier and cursor-restore gaps; run 3 (this release) 96.9%
  (31.0/32), zero fail signals, with all three run-2 gaps verified fixed
  by graders reading the generated code. Cross-model check on Codex CLI
  0.157.1 (gpt-6-luna, same scenarios and rubrics): 81.2%, with the
  skill's new guidance verified to transfer (no concept-level failures).
- Full pipeline green: markdownlint, mockup alignment, cross-refs, evals,
  install simulation, compatibility, 40+ script unit tests, template
  compiles, both example projects' test suites (dbview-go, log-monitor-rust
  24/24).

## [0.1.0] — 2025-11-13

Initial release: Claude Code plugin + self-hosted marketplace, skills pack
for OpenCode/Codex/ZCode, 15 reference documents, 4 framework guides, 6
screen patterns, 4 runnable starter templates, and the dbview-go /
log-monitor-rust example projects.

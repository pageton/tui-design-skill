# Eval: Framework Selection — High-Throughput Log Monitor

## Category

`framework-selection`

## Prompt

We're building an internal log-tailing monitor: it streams thousands of
lines per second, runs on servers people reach over SSH and sometimes inside
tmux, and the team knows TypeScript and Rust well (no Go, no Python). Which
TUI framework should we use? Don't give me a generic list — decide.

## Fixture

None — greenfield decision question, empty directory.

## Pass Criteria

- Gives a decisive recommendation tied to the stated requirements — no
  "it depends", no popularity ranking.
- Names the 2-3 requirements that decided it (throughput, SSH/tmux
  constraints, language fit), the runner-up framework, and the limitations
  that will bite the chosen one.
- Compares the candidates on the axes that matter here: rendering model
  under high-frequency updates, terminal/tmux compatibility, Unicode
  handling, testability.
- Notes that no framework implements BiDi if Arabic logs are ever in scope,
  and states a minimum terminal contract.
- The reasoning survives the follow-up "why not Ink?" without contradicting
  the original analysis.

## Fail Signals

- Recommends a framework in a language the team doesn't use.
- Ranks frameworks "overall" instead of against these requirements.
- Ignores the throughput or SSH/tmux constraints.
- No runner-up and no stated limitations.

## References Expected

- `references/framework-selection.md`

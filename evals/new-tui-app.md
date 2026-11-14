# Eval: New TUI — Server Health Dashboard

## Category

`new-tui`

## Prompt

Build me a server health dashboard TUI in Go. It shows CPU, memory, and disk
usage plus a list of services with up/down status, and a detail pane for the
selected service. Stats come from polling `http://localhost:9090/metrics`
every 2 seconds. Our team uses this all day, so it needs to feel polished —
not like a debug console.

## Fixture

Empty project: a `go.mod` (`module healthdash`, Go 1.25) and nothing else. No
framework chosen yet.

## Pass Criteria

- Asks at most one short round of clarification, then presents a concrete
  design (screens, layout, keys) before generating code.
- Shows the layout as an ASCII mockup whose frame lines all align at one
  fixed width.
- Architecture separates model, update, and view (or equivalent framework
  idiom) — no monolithic render file; no business logic inside view code.
- Polling runs as a command/effect (e.g. `tea.Cmd`), never inside update or
  view; failures surface as a designed error view with a retry action.
- Ships designed states from the start: loading skeleton, empty service
  list, error banner — not blank panes.
- Footer/status bar with key hints; a stated minimum size with a polite
  message below it; resize recomputes layout.
- Includes headless tests: state transitions plus a render smoke test at
  fixed dimensions — and runs them before claiming done.

## Fail Signals

- Single-file app with HTTP calls inside the render path.
- No loading/empty/error states, or states added only after prompting.
- Mockup that misaligns, or no layout proposal at all.
- Hardcoded terminal width; no key hints; min size undefined.
- Claims completion without running tests, or ships no tests.

## References Expected

- `references/design-principles.md`
- `references/architecture-patterns.md`
- `references/states-and-feedback.md`
- `references/testing-tuis.md`
- `frameworks/bubbletea-go.md`

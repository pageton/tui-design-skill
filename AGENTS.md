# AGENTS.md

## What This Repo Is

A Claude Code plugin (with a skills pack alongside it for OpenCode, Codex, ZCode, and any Agent Skills-compliant tool). No build step, no runtime — all files are prose references, command definitions, and starter templates. `CLAUDE.md` is an older, smaller subset; this file is authoritative.

## Verification

Run `just check-all` before committing. Individual recipes:

- `lint-md` — markdownlint over `skills/tui-design/references skills/tui-design/frameworks skills/tui-design/patterns skills/tui-design/projects skills/tui-design/SKILL.md README.md commands opencode/commands codex/commands zcode/commands`
- `check-mockups` — `scripts/check-mockups.py` (fixed-width mockup enforcement)
- `check-rust` / `check-go` / `check-python` — starter templates compile/vet/py_compile
- `check-go-project` / `check-rust-project` — example projects compile and pass tests
- `build-rust` / `build-go` / `clean` — build templates, clean artifacts

Gotchas an agent will otherwise guess wrong:

- `.markdownlint.json` disables MD013 (line length) and MD040 (code-fence language). Long lines and bare code fences are intentional — do not "fix" them.
- `check-mockups` scans every `.md` in the checked dirs: all frame lines of a mockup must be equal width and a status bar must match its frame. A misaligned mockup is worse than no mockup.
- Display-width claims in `skills/tui-design/references/unicode-and-text.md` must be verified with a real width library (e.g. `string-width` from `skills/tui-design/templates/ink-starter/node_modules`), never counted by hand.

## Editing Constraints

- **Mockups render at fixed width.** Use box-drawing chars (`─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴`) or ASCII (`+ - |`) consistently within one mockup; status bar width = frame width. Verify with `just check-mockups`.
- **Component numbering in `skills/tui-design/references/component-catalog.md`** is cross-referenced elsewhere. Continue the numbering; never renumber existing entries.
- **Starter templates must run as-is** — no placeholder pseudocode. Verify with the toolchain before changing:
  - `skills/tui-design/templates/bubbletea-starter/` — `go run main.go` (Go 1.25+, Bubble Tea v1.3, Lip Gloss v1.1)
  - `skills/tui-design/templates/textual-starter/` — `textual run app.py --dev` (Textual pip package)
  - `skills/tui-design/templates/ratatui-starter/` — `cargo run` (edition 2021, Ratatui 0.29, Crossterm 0.28)
  - `skills/tui-design/templates/ink-starter/` — `npm start` (Node.js, Ink ^5.2, React ^18.3)
- **Example projects must compile and pass unit tests** — they are the reference implementations of `skills/tui-design/references/advanced-patterns.md` and `skills/tui-design/references/stability-and-robustness.md`; keep them in sync when those references change:
  - `skills/tui-design/projects/dbview-go/` — `go vet ./... && go test ./...` (headless; no TTY needed)
  - `skills/tui-design/projects/log-monitor-rust/` — `cargo check && cargo test`
  - Never weaken a test to make the pipeline green — fix the app.
- **Framework guides share a skeleton:** overview → architecture → project structure → framework sections (styling, keybindings, async, components) → best practices/common mistakes → dependencies. Keep that shape in `skills/tui-design/frameworks/*.md`.

## Architecture

- `.claude-plugin/plugin.json` — Claude Code plugin manifest. `skills` points at `./skills/`; `commands` lists the plugin slash command.
- `.claude-plugin/marketplace.json` — lets this repo serve as its own marketplace (`/plugin marketplace add pageton/tui-design-skill`).
- `skills/tui-design/SKILL.md` — authoritative skill definition (triggers, principles, workflows, standards). The frontmatter `name`/`description` is required for skill discovery by agents.
- `commands/tui-design.md` — Claude Code plugin command; delegates to the `tui-design` skill, no hardcoded install path.
- `opencode/commands/`, `codex/commands/`, `zcode/commands/` — per-tool command files that delegate to the installed skills pack.
- `skills/tui-design/references/` — self-contained design docs loaded on demand; one concern per file.
- `skills/tui-design/frameworks/` — one guide per framework. `skills/tui-design/patterns/` — screen-pattern templates. `skills/tui-design/templates/` — runnable starters. `skills/tui-design/projects/` — reference implementations.

## Cross-Reference Maintenance (easy to miss)

The Claude Code plugin loads `skills/tui-design/` directly; OpenCode/Codex/ZCode install a copy of the same directory (and `npx skills add` discovers `skills/tui-design/SKILL.md`). When adding, renaming, or removing a reference file, update in the same change:

1. `skills/tui-design/SKILL.md` → "Reference Documents" list
2. `README.md` → "What's Included" tree (and install instructions if paths changed)

When the pack layout changes, keep the four command files (`commands/`, `opencode/commands/`, `codex/commands/`, `zcode/commands/`) in sync.

## Installation

- **Claude Code:** plugin install via the marketplace mechanism: `/plugin marketplace add pageton/tui-design-skill`, then `/plugin install tui-design`. Local dev: `claude --plugin-dir .` at the repo root.
- **Other agents:** `npx skills add pageton/tui-design-skill` (the `vercel-labs/skills` CLI; auto-detects agents, symlinks the pack) or copy `skills/tui-design/{SKILL.md,references,frameworks,patterns,templates,projects}` into the agent's skills dir, plus that tool's command file (`opencode/commands/`, `codex/commands/`, `zcode/commands/`). Exact paths: `README.md`.

## Design Principles (Non-Negotiable)

Encoded across the skill files; preserve in any edits:

1. Start monochrome; add color only where it earns its place (max 3-4 colors)
2. Generous spacing (min 1 cell inside borders, prefer 2); tight spacing is a design smell
3. Keyboard-first navigation with visible key hints in a status bar/footer
4. All states designed: empty, loading, error, interactive — never afterthoughts
5. Composable architecture: separate domain, state, view, and input handling
6. Responsive to terminal resize; define minimum dimensions

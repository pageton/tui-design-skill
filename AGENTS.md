# AGENTS.md

## What This Repo Is

A Markdown-only skill pack consumed by AI coding tools (Claude Code, OpenCode). Not a buildable software project — all files are prose references, command definitions, and starter templates. Validation is `just check-all`: markdownlint, ASCII mockup width checks (`scripts/check-mockups.py`), and compile checks for the starter templates.

## Editing Constraints

- **ASCII mockups must render at fixed width.** Use box-drawing characters (Unicode `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴` or ASCII `+ - |`) consistently within each mockup, and keep the status bar the same width as the frame it belongs to. Verify with `just check-mockups` (runs `scripts/check-mockups.py`) before committing — a misaligned mockup is worse than no mockup.
- **Component numbering in `references/component-catalog.md`** is cross-referenced. When adding components, continue the existing numbering scheme. Do not renumber existing entries.
- **Starter templates in `templates/` must be runnable as-is.** No placeholder pseudocode. Verify with the framework toolchain before changing:
  - `templates/bubbletea-starter/` — `go run main.go` (requires Go 1.25+, Bubble Tea v1.3, Lip Gloss v1.1)
  - `templates/textual-starter/` — `textual run app.py --dev` (requires Textual pip package)
  - `templates/ratatui-starter/` — `cargo run` (requires Rust edition 2021, Ratatui 0.29, Crossterm 0.28)
  - `templates/ink-starter/` — `npm start` (requires Node.js, Ink ^5.2, React ^18.3)
- **Framework guides share a common skeleton:** overview → architecture → project structure → framework-specific sections (styling, keybindings, async, components — named per framework idiom) → best practices/common mistakes → dependencies. Keep that shape when editing `frameworks/*.md`.

## Architecture

- `SKILL.md` — Authoritative skill definition. Triggers, principles, workflows, and output standards all live here.
- `commands/` — Thin entry points that point the tool at the installed skill pack. Both assume the pack is installed (OpenCode: `~/.config/opencode/skills/tui-design/`, Claude Code: `~/.claude/skills/tui-design/`); they differ only in install paths and frontmatter.
- `scripts/` — Validation helpers. `check-mockups.py` enforces fixed-width ASCII mockups.
- `references/` — Standalone design reference docs loaded on demand. Each file is self-contained.
- `frameworks/` — Framework-specific guides. One per framework (Bubble Tea, Textual, Ratatui, Ink).
- `patterns/` — Screen pattern templates with ASCII layouts. Each follows the same structure: description, layout mockup, component breakdown, keybindings, states.
- `templates/` — Complete runnable starter apps (bubbletea-starter, textual-starter, ratatui-starter, ink-starter). Each is a minimal but real implementation of the skill's design principles.

## Design Principles (Non-Negotiable)

These are encoded across the skill files and must be preserved in any edits:

1. Start monochrome; add color only where it earns its place (max 3-4 colors)
2. Generous spacing (min 1 cell inside borders, prefer 2); tight spacing is a design smell
3. Keyboard-first navigation with visible key hints in a status bar/footer
4. All states designed: empty, loading, error, interactive — never afterthoughts
5. Composable architecture: separate domain, state, view, and input handling
6. Responsive to terminal resize; define minimum dimensions

## Installation (from README)

Installation is file copying — no package manager or build step:

- **OpenCode:** Copy `SKILL.md` + `references/` + `frameworks/` + `patterns/` + `templates/` into `~/.config/opencode/skills/tui-design/`. Copy `commands/opencode-tui-design.md` into `~/.config/opencode/commands/tui-design.md`.
- **Claude Code:** Copy the same skill pack into `~/.claude/skills/tui-design/`. Copy `commands/claude-code-tui-design.md` into `~/.claude/commands/tui-design.md`.

When updating the skill, both install targets may need updating. Both commands delegate to the installed skill pack — neither is self-contained — so the pack must be installed for the slash command to work.

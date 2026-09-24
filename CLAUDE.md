# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A skill pack for building polished TUIs. Not a buildable software project — it's a collection of Markdown reference documents, command definitions, and starter templates consumed by AI coding tools (Claude Code, Codex, OpenCode, ZCode). Validation is `just check-all` (markdownlint, ASCII mockup widths, template compile checks, example project tests) — see `AGENTS.md`.

## Repository Structure

- `SKILL.md` — Main skill definition: triggers, principles, workflows, output standards
- `commands/` — Tool-specific slash command entry points (Claude Code, OpenCode, Codex, ZCode)
- `references/` — Design reference docs (design-principles, architecture-patterns, framework-selection, terminal-compatibility, unicode-and-text, rtl-and-bidi, testing-tuis, troubleshooting, interaction-guide, component-catalog, color-and-emphasis, states-and-feedback, advanced-patterns, stability-and-robustness, review-checklist)
- `frameworks/` — Framework-specific guides for Bubble Tea (Go), Textual (Python), Ratatui (Rust), Ink (TypeScript)
- `patterns/` — Screen pattern templates with ASCII layouts: dashboard, data-browser, form-workflow, log-viewer, file-explorer
- `templates/` — Runnable starter apps for each framework (`bubbletea-starter/`, `textual-starter/`, `ratatui-starter/`, `ink-starter/`)

## Editing Guidelines

- All content is Markdown. Keep formatting consistent with existing files.
- Framework guides follow a standard structure: overview → architecture → project structure → framework sections (styling, keybindings, async, components) → best practices/common mistakes → dependencies.
- ASCII mockups use box-drawing characters (`+`, `-`, `|`, `>`) and must render correctly at fixed width.
- Component patterns in `references/component-catalog.md` include numbered mockup examples — maintain that numbering when adding components.
- Starter templates in `templates/` must be runnable as-is with their respective framework's toolchain (`go run`, `textual run`, `cargo run`, `npm start`).

## Key Design Principles (encoded across the skill)

- Start monochrome; add color only where it earns its place
- Generous spacing (min 1 cell inside borders, prefer 2); tight spacing is a design smell
- Keyboard-first navigation with visible key hints in a status bar/footer
- All states designed: empty, loading, error, interactive — never afterthoughts
- Composable architecture: separate domain, state, view, and input handling
- Responsive to terminal resize; define minimum dimensions

## Installation

Install via `npx skills add pageton/tui-design-skill` (auto-detects installed agents) or by copying files into tool config directories — see `README.md` for the exact paths. Each tool gets the pack (`SKILL.md` + `references/` + `frameworks/` + `patterns/` + `templates/` + `projects/`) plus its command file: Claude Code → `~/.claude/commands/tui-design.md`, OpenCode → `~/.config/opencode/commands/tui-design.md`, Codex → `~/.codex/prompts/tui-design.md`, ZCode → `~/.zcode/commands/tui-design.md`.

## License

MIT — see `LICENSE`.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A skill pack for building polished TUIs. Not a buildable software project — it's a collection of Markdown reference documents, command definitions, and starter templates consumed by AI coding tools (Claude Code, OpenCode). There are no build steps, tests, or linting.

## Repository Structure

- `SKILL.md` — Main skill definition: triggers, principles, workflows, output standards
- `commands/` — Tool-specific slash command entry points (`claude-code-tui-design.md` for Claude Code, `opencode-tui-design.md` for OpenCode)
- `references/` — Design reference docs (design-principles, architecture-patterns, interaction-guide, component-catalog, color-and-emphasis, states-and-feedback, review-checklist)
- `frameworks/` — Framework-specific guides for Bubble Tea (Go), Textual (Python), Ratatui (Rust), Ink (TypeScript)
- `patterns/` — Screen pattern templates with ASCII layouts: dashboard, data-browser, form-workflow, log-viewer, file-explorer
- `templates/` — Runnable starter apps for each framework (`bubbletea-starter/`, `textual-starter/`, `ratatui-starter/`, `ink-starter/`)

## Editing Guidelines

- All content is Markdown. Keep formatting consistent with existing files.
- Framework guides follow a standard structure: overview, architecture, core interface, styling, common patterns, gotchas.
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

The skill is installed by copying files into tool config directories — see `README.md` for the exact paths. Claude Code uses `commands/claude-code-tui-design.md` copied to `~/.claude/commands/tui-design.md`. OpenCode uses `SKILL.md`, `references/`, `frameworks/`, `patterns/`, `templates/`, and `commands/opencode-tui-design.md` copied to `~/.config/opencode/skills/tui-design/` and `~/.config/opencode/commands/tui-design.md` respectively.

# TUI Design Skill

A production-grade AI skill for designing and building exceptionally polished terminal user interfaces. Works as an expert terminal product designer and senior TUI engineer — opinionated about good design, strong on architecture, and focused on making terminal apps feel modern and delightful.

## What It Does

- **Generate** new TUI apps from a product idea
- **Convert** CLI workflows into interactive TUIs
- **Redesign** existing TUIs to feel modern and polished
- **Review** TUI code with a scored UX assessment
- **Recommend** frameworks, patterns, and components

## Install

Clone or download this repo, then install into your tool(s) of choice.

### Quick Install (both tools)

```bash
# Clone the skill
git clone https://github.com/pageton/tui-design-skill ~/Projects/tui-design-skill

# Install for OpenCode
mkdir -p ~/.config/opencode/skills/tui-design
cp -r ~/Projects/tui-design-skill/references ~/.config/opencode/skills/tui-design/
cp -r ~/Projects/tui-design-skill/frameworks ~/.config/opencode/skills/tui-design/
cp -r ~/Projects/tui-design-skill/patterns ~/.config/opencode/skills/tui-design/
cp -r ~/Projects/tui-design-skill/templates ~/.config/opencode/skills/tui-design/
cp ~/Projects/tui-design-skill/SKILL.md ~/.config/opencode/skills/tui-design/SKILL.md
mkdir -p ~/.config/opencode/commands
cp ~/Projects/tui-design-skill/commands/opencode-tui-design.md ~/.config/opencode/commands/tui-design.md

# Install for Claude Code
mkdir -p ~/.claude/skills/tui-design
cp -r ~/Projects/tui-design-skill/references ~/.claude/skills/tui-design/
cp -r ~/Projects/tui-design-skill/frameworks ~/.claude/skills/tui-design/
cp -r ~/Projects/tui-design-skill/patterns ~/.claude/skills/tui-design/
cp -r ~/Projects/tui-design-skill/templates ~/.claude/skills/tui-design/
cp ~/Projects/tui-design-skill/SKILL.md ~/.claude/skills/tui-design/SKILL.md
mkdir -p ~/.claude/commands
cp ~/Projects/tui-design-skill/commands/claude-code-tui-design.md ~/.claude/commands/tui-design.md
```

### OpenCode

1. Copy the skill to your OpenCode skills directory:

   ```bash
   mkdir -p ~/.config/opencode/skills/tui-design
   cp -r ~/Projects/tui-design-skill/{SKILL.md,references,frameworks,patterns,templates} \
       ~/.config/opencode/skills/tui-design/
   ```

2. Copy the command file:

   ```bash
   cp ~/Projects/tui-design-skill/commands/opencode-tui-design.md \
       ~/.config/opencode/commands/tui-design.md
   ```

3. Invoke with:

   ```
   /tui-design Build me a dashboard for monitoring server health
   ```

### Claude Code

1. Copy the skill pack so the command can load the reference files:

   ```bash
   mkdir -p ~/.claude/skills/tui-design
   cp -r ~/Projects/tui-design-skill/{SKILL.md,references,frameworks,patterns,templates} \
       ~/.claude/skills/tui-design/
   ```

2. Copy the command file:

   ```bash
   mkdir -p ~/.claude/commands
   cp ~/Projects/tui-design-skill/commands/claude-code-tui-design.md \
       ~/.claude/commands/tui-design.md
   ```

3. Invoke with:

   ```
   /tui-design Build me a dashboard for monitoring server health
   ```

### From skill.zip

```bash
# Unzip to a temporary location
unzip skill.zip -d ~/Projects/tui-design-skill

# Then follow the OpenCode and/or Claude Code steps above
```

## What's Included

```
tui-design-skill/
├── SKILL.md                          # Main skill definition
├── commands/                         # Tool-specific command files
│   ├── claude-code-tui-design.md     # Claude Code slash command
│   └── opencode-tui-design.md        # OpenCode slash command
├── references/                       # Design reference documents
│   ├── design-principles.md          # Visual hierarchy, spacing, layout
│   ├── architecture-patterns.md      # State management, components, async
│   ├── interaction-guide.md          # Keybindings, focus, navigation
│   ├── component-catalog.md          # 14 component patterns with mockups
│   ├── color-and-emphasis.md         # Palette strategy, terminal compat
│   ├── states-and-feedback.md        # Empty/loading/error state patterns
│   └── review-checklist.md           # 10-category scored UX review
├── frameworks/                       # Framework-specific guides
│   ├── bubbletea-go.md               # Go + Bubble Tea + Lip Gloss
│   ├── textual-python.md             # Python + Textual
│   ├── ratatui-rust.md               # Rust + Ratatui + Crossterm
│   └── ink-react.md                  # TypeScript + Ink + React
├── patterns/                         # Screen patterns with ASCII layouts
│   ├── dashboard.md
│   ├── data-browser.md
│   ├── form-workflow.md
│   ├── log-viewer.md
│   └── file-explorer.md
├── scripts/
│   └── check-mockups.py              # ASCII mockup alignment checker (just check-mockups)
└── templates/                        # Runnable starter apps
    ├── bubbletea-starter/main.go
    ├── textual-starter/app.py
    ├── ratatui-starter/
    │   ├── Cargo.toml
    │   └── src/main.rs
    └── ink-starter/
        ├── package.json
        ├── tsconfig.json
        └── src/main.tsx
```

## Example Prompts

- `Build me a beautiful TUI for browsing database records`
- `Turn this CLI deployment tool into a polished interactive TUI`
- `Redesign this Bubble Tea app so it feels premium`
- `Create a dashboard-style terminal UI with panels and keyboard navigation`
- `Review my Textual app and make the UX much better`
- `Generate a clean multi-pane log viewer TUI`
- `Design a gorgeous terminal file explorer`
- `Make this admin TUI less ugly and more modern`

## Design Philosophy

The skill is opinionated about these defaults:

- **Start monochrome** — add color only where it earns its place
- **Generous spacing** — tight spacing signals amateur design
- **Keyboard-first** — all actions reachable via keyboard, with visible key hints
- **Designed states** — empty, loading, error, and interactive states are never afterthoughts
- **Composable architecture** — separate domain, state, and view logic
- **Responsive** — handle terminal resize gracefully, define minimum sizes

## Framework Support

| Framework | Language | Best For |
|-----------|----------|----------|
| Bubble Tea + Lip Gloss | Go | DevOps tools, CLIs, single-binary utilities |
| Textual | Python | Data tools, dashboards, admin panels |
| Ratatui + Crossterm | Rust | High-performance tools, long-running monitors |
| Ink + React | TypeScript | Interactive CLIs, dev tools, JS-native workflows |

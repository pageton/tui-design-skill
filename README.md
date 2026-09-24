# TUI Design Skill

A production-grade AI skill for designing and building exceptionally polished terminal user interfaces. Works as an expert terminal product designer and senior TUI engineer — opinionated about good design, strong on architecture, and focused on making terminal apps feel modern and delightful.

## What It Does

- **Generate** new TUI apps from a product idea
- **Convert** CLI workflows into interactive TUIs
- **Redesign** existing TUIs to feel modern and polished
- **Review** TUI code with a scored UX assessment
- **Recommend** frameworks, patterns, and components
- **Handle** Unicode/RTL text, terminal compatibility, and testing correctly

## Install

### Claude Code

Installed as a plugin, through the normal marketplace mechanism. No manual file copying.

**1. Add this repo as a marketplace:**

```
/plugin marketplace add pageton/tui-design-skill
```

**2. Install the plugin:**

```
/plugin install tui-design
```

**3. Invoke with:**

```
/tui-design Build me a dashboard for monitoring server health
```

Or just describe a TUI task in conversation — the skill triggers automatically.

To test a local checkout before publishing, run Claude Code with `--plugin-dir` pointed at the repo:

```
claude --plugin-dir ~/Projects/tui-design-skill
```

### Other agents (OpenCode, Codex, ZCode, …)

The pack works with any tool that follows the [Agent Skills
specification](https://agentskills.io). Install it with the skills CLI
(recommended) or copy files manually per tool.

#### Via the skills CLI (recommended)

```bash
# One command — auto-detects your installed agents (OpenCode, Codex,
# ZCode, Cursor, …) and installs for all of them
npx skills add pageton/tui-design-skill

# Global install (available in all projects) for specific agents
npx skills add pageton/tui-design-skill -g -a opencode -a codex -a zcode

# Non-interactive (CI friendly)
npx skills add pageton/tui-design-skill -g -y
```

The CLI (`vercel-labs/skills`) symlinks the pack into each agent's skills
directory, so `npx skills update` keeps every agent on the latest version.
To use the slash-command entry point (optional — the skill also activates
automatically), copy the command file as shown below.

#### Manual install per agent

Clone or download the repo first:

```bash
git clone https://github.com/pageton/tui-design-skill ~/Projects/tui-design-skill
```

Then install the pack (skill) and the slash command for each tool:

```bash
# OpenCode
mkdir -p ~/.config/opencode/skills/tui-design
cp -r ~/Projects/tui-design-skill/skills/tui-design/{SKILL.md,references,frameworks,patterns,templates,projects} \
    ~/.config/opencode/skills/tui-design/
mkdir -p ~/.config/opencode/commands
cp ~/Projects/tui-design-skill/opencode/commands/tui-design.md ~/.config/opencode/commands/tui-design.md
# Invoke: /tui-design Build me a dashboard for monitoring server health

# Codex
mkdir -p ~/.codex/skills/tui-design
cp -r ~/Projects/tui-design-skill/skills/tui-design/{SKILL.md,references,frameworks,patterns,templates,projects} \
    ~/.codex/skills/tui-design/
mkdir -p ~/.codex/prompts
cp ~/Projects/tui-design-skill/codex/commands/tui-design.md ~/.codex/prompts/tui-design.md
# Invoke: /prompts:tui-design Build me a dashboard for monitoring server health

# ZCode
mkdir -p ~/.zcode/skills/tui-design
cp -r ~/Projects/tui-design-skill/skills/tui-design/{SKILL.md,references,frameworks,patterns,templates,projects} \
    ~/.zcode/skills/tui-design/
mkdir -p ~/.zcode/commands
cp ~/Projects/tui-design-skill/zcode/commands/tui-design.md ~/.zcode/commands/tui-design.md
# Invoke: /tui-design Build me a dashboard for monitoring server health
```

## What's Included

```
tui-design-skill/
├── .claude-plugin/
│   ├── plugin.json                   # Claude Code plugin manifest
│   └── marketplace.json              # Lets this repo self-host as a marketplace
├── AGENTS.md                         # Editing constraints for AI coding agents
├── commands/
│   └── tui-design.md                 # Claude Code plugin slash command
├── opencode/
│   └── commands/
│       └── tui-design.md             # OpenCode slash command
├── codex/
│   └── commands/
│       └── tui-design.md             # Codex slash command
├── zcode/
│   └── commands/
│       └── tui-design.md             # ZCode slash command
├── skills/
│   └── tui-design/
│       ├── SKILL.md                  # Main skill definition
│       ├── references/               # Design reference documents
│       │   ├── design-principles.md          # Visual hierarchy, spacing, layout
│       │   ├── architecture-patterns.md      # State management, components, async
│       │   ├── framework-selection.md        # Framework trade-off matrix + decision rules
│       │   ├── terminal-compatibility.md     # Terminal capability matrix + fallbacks
│       │   ├── unicode-and-text.md           # Display width, Unicode cases and tests
│       │   ├── rtl-and-bidi.md               # Arabic/RTL logical-vs-visual rules
│       │   ├── testing-tuis.md               # Unit/snapshot/interaction/Unicode tests
│       │   ├── troubleshooting.md            # Symptom → layer attribution → fix
│       │   ├── interaction-guide.md          # Keybindings, focus, navigation
│       │   ├── component-catalog.md          # 14 component patterns with mockups
│       │   ├── color-and-emphasis.md         # Palette strategy, terminal compat
│       │   ├── states-and-feedback.md        # Empty/loading/error state patterns
│       │   ├── advanced-patterns.md          # Grids, pagination, filtering, theming
│       │   ├── stability-and-robustness.md   # Resize, panics, async safety, backpressure
│       │   └── review-checklist.md           # 10-category scored UX review
│       ├── frameworks/               # Framework-specific guides
│       │   ├── bubbletea-go.md               # Go + Bubble Tea + Lip Gloss
│       │   ├── textual-python.md             # Python + Textual
│       │   ├── ratatui-rust.md               # Rust + Ratatui + Crossterm
│       │   └── ink-react.md                  # TypeScript + Ink + React
│       ├── patterns/                 # Screen patterns with ASCII layouts
│       │   ├── dashboard.md
│       │   ├── data-browser.md
│       │   ├── database-browser.md           # dbview-style multi-view data tool
│       │   ├── form-workflow.md
│       │   ├── log-viewer.md
│       │   └── file-explorer.md
│       ├── templates/                # Runnable starter apps
│       │   ├── bubbletea-starter/main.go
│       │   ├── textual-starter/app.py
│       │   ├── ratatui-starter/
│       │   │   ├── Cargo.toml
│       │   │   └── src/main.rs
│       │   └── ink-starter/
│       │       ├── package.json
│       │       ├── package-lock.json
│       │       ├── tsconfig.json
│       │       └── src/main.tsx
│       └── projects/                 # Complete runnable example apps
│           ├── dbview-go/                    # Advanced data browser (Bubble Tea)
│           │   ├── main.go                   #   model, view stack, layout math
│           │   ├── update.go                 #   key routing: modal > input > view
│           │   ├── store.go                  #   typed filter/sort/paginate domain
│           │   ├── view.go                   #   grid, status bar, modals, themes
│           │   ├── theme.go                  #   runtime-switchable palettes
│           │   └── *_test.go                 #   logic + render smoke tests
│           └── log-monitor-rust/             # Resilient log streamer (Ratatui)
│               ├── src/main.rs               #   panic-safe terminal guard + loop
│               ├── src/app.rs                #   input model (unit-tested)
│               ├── src/ring.rs               #   bounded buffer w/ drop accounting
│               ├── src/stream.rs             #   simulated producer
│               └── src/ui.rs                 #   stats, viewport, banners
├── scripts/
│   └── check-mockups.py              # ASCII mockup alignment checker
└── justfile                          # Validation pipeline (just check-all)
```

## Development

No build step — the repo is Markdown plus starter templates, validated with [just](https://github.com/casey/just):

```bash
just check-all      # markdownlint + mockup widths + template compile checks
just check-mockups  # ASCII mockup alignment only
```

`check-all` enforces the repo's own quality rules: every ASCII mockup must render at a fixed width (a misaligned mockup is worse than no mockup — see `AGENTS.md`), markdown must lint clean, the Bubble Tea, Ratatui, and Textual templates must compile, and the example projects must compile *and pass their unit tests*. Each starter also runs directly:

```bash
cd skills/tui-design/templates/bubbletea-starter && go run main.go
cd skills/tui-design/templates/textual-starter   && textual run app.py --dev
cd skills/tui-design/templates/ratatui-starter   && cargo run
cd skills/tui-design/templates/ink-starter       && npm install && npm start
```

## Example Projects

Beyond the minimal starters, `skills/tui-design/projects/` contains complete
apps that show how the references hold up in real code:

| Project | Stack | Focus |
|---------|-------|-------|
| [dbview-go](skills/tui-design/projects/dbview-go/) | Go + Bubble Tea + Lip Gloss | Advanced data-app patterns: multi-view stack, pagination, typed sorting, live AND-filtering with history, confirm-before-delete, theme cycling — modeled on [dbview](https://github.com/pageton/dbview) |
| [log-monitor-rust](skills/tui-design/projects/log-monitor-rust/) | Rust + Ratatui + Crossterm | Stability: backpressure with drop accounting, pause/resume, disconnect/retry, panic-safe terminal restore, min-size gate |

Both ship unit tests that verify the stability contract without a TTY
(`just check-go-project`, `just check-rust-project`).

## Example Prompts

- `Build me a beautiful TUI for browsing database records`
- `Build a dbview-style database explorer with sorting, filtering, and query history`
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

## License

MIT — see [LICENSE](LICENSE).

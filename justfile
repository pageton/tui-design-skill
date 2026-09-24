# TUI Design Skill — Validation Pipeline
# Run: just check-all

# --- Configuration ---

md_dirs := "skills/tui-design/references skills/tui-design/frameworks skills/tui-design/patterns skills/tui-design/projects skills/tui-design/SKILL.md README.md commands opencode/commands codex/commands zcode/commands"

# --- Composite targets ---

# Run all validation checks
check-all: lint-md check-mockups check-rust check-go check-python check-go-project check-rust-project
    @echo "All checks passed."

# --- Individual checks ---

# Lint all markdown files
lint-md:
    markdownlint {{md_dirs}}

# Check all ASCII mockups render at fixed width
check-mockups:
    python3 scripts/check-mockups.py

# Check Rust template compiles
check-rust:
    cd skills/tui-design/templates/ratatui-starter && RUSTC_WRAPPER="" cargo check 2>&1

# Check Go template compiles and vets clean
check-go:
    cd skills/tui-design/templates/bubbletea-starter && go vet ./...

# Check Python template for syntax errors
check-python:
    python3 -m py_compile skills/tui-design/templates/textual-starter/app.py

# Check example projects compile and pass their unit tests
check-go-project:
    cd skills/tui-design/projects/dbview-go && go vet ./... && go test ./... -count=1 2>&1

check-rust-project:
    cd skills/tui-design/projects/log-monitor-rust && RUSTC_WRAPPER="" cargo check 2>&1 && RUSTC_WRAPPER="" cargo test --quiet 2>&1

# --- Build (compile all templates) ---

build-rust:
    cd skills/tui-design/templates/ratatui-starter && RUSTC_WRAPPER="" cargo build 2>&1

build-go:
    cd skills/tui-design/templates/bubbletea-starter && go build -o /dev/null ./...

# --- Clean ---

clean:
    cd skills/tui-design/templates/ratatui-starter && RUSTC_WRAPPER="" cargo clean 2>/dev/null || true
    rm -f skills/tui-design/templates/bubbletea-starter/tui-starter 2>/dev/null || true

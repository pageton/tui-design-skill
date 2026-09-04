# TUI Design Skill — Validation Pipeline
# Run: just check-all

# --- Configuration ---

md_dirs := "references frameworks patterns projects SKILL.md README.md commands"

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
    cd templates/ratatui-starter && RUSTC_WRAPPER="" cargo check 2>&1

# Check Go template compiles and vets clean
check-go:
    cd templates/bubbletea-starter && go vet ./...

# Check Python template for syntax errors
check-python:
    python3 -m py_compile templates/textual-starter/app.py

# Check example projects compile and pass their unit tests
check-go-project:
    cd projects/dbview-go && go vet ./... && go test ./... -count=1 2>&1

check-rust-project:
    cd projects/log-monitor-rust && RUSTC_WRAPPER="" cargo check 2>&1 && RUSTC_WRAPPER="" cargo test --quiet 2>&1

# --- Build (compile all templates) ---

build-rust:
    cd templates/ratatui-starter && RUSTC_WRAPPER="" cargo build 2>&1

build-go:
    cd templates/bubbletea-starter && go build -o /dev/null ./...

# --- Clean ---

clean:
    cd templates/ratatui-starter && RUSTC_WRAPPER="" cargo clean 2>/dev/null || true
    rm -f templates/bubbletea-starter/tui-starter 2>/dev/null || true

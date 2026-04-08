# TUI Design Skill — Validation Pipeline
# Run: just check-all

# --- Configuration ---

md_dirs := "references frameworks patterns SKILL.md README.md commands"

# --- Composite targets ---

# Run all validation checks
check-all: lint-md check-rust check-go check-python
    @echo "All checks passed."

# --- Individual checks ---

# Lint all markdown files
lint-md:
    markdownlint {{md_dirs}}

# Check Rust template compiles
check-rust:
    cd templates/ratatui-starter && cargo check 2>&1

# Check Go template compiles
check-go:
    cd templates/bubbletea-starter && go build -o /dev/null ./...

# Check Python template for syntax errors
check-python:
    python3 -m py_compile templates/textual-starter/app.py

# --- Build (compile all templates) ---

build-rust:
    cd templates/ratatui-starter && cargo build 2>&1

build-go:
    cd templates/bubbletea-starter && go build -o /dev/null ./...

# --- Clean ---

clean:
    cd templates/ratatui-starter && cargo clean 2>/dev/null || true
    rm -f templates/bubbletea-starter/tui-starter templates/bubbletea-starter/go.sum 2>/dev/null || true

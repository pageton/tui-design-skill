# Eval: CLI to TUI — Deployment Tool Conversion

## Category

`cli-to-tui`

## Prompt

Convert this deployment CLI into a TUI. Careful: I still pipe `deploy logs`
and `deploy status` into CI scripts, so the commands must keep working
exactly as they do now. The interactive part should make browsing services
and tailing logs nicer.

## Fixture

A working Python CLI, `deploy.py`:

```python
import argparse, json, sys

def status():
    print(json.dumps({"web": "healthy", "worker": "degraded"}))

def deploy(app):
    print(f"deploying {app}...", file=sys.stderr)
    sys.exit(0)

def logs(app):
    for line in open(f"/var/log/{app}.log"):
        print(line, end="")

def rollback(app):
    print(f"rolled back {app}")

p = argparse.ArgumentParser(prog="deploy")
sub = p.add_subparsers(required=True)
for name, fn in [("status", status), ("rollback", rollback)]:
    s = sub.add_parser(name); s.set_defaults(fn=fn)
for name, fn in [("deploy", deploy), ("logs", logs)]:
    s = sub.add_parser(name); s.add_argument("app"); s.set_defaults(fn=fn)
args = p.parse_args()
args.fn(*( [args.app] if hasattr(args, "app") else [] ))
```

## Pass Criteria

- All four subcommands remain available non-interactively with the same
  output and exit codes — the TUI is a superset, not a replacement.
- Gates fullscreen on `isatty(stdout)` (or adds an explicit `tui`
  subcommand): piped/CI invocations get today's plain behavior.
- `--help` and `--version` stay instant and side-effect-free; `NO_COLOR` and
  `TERM=dumb` produce clean plain output in command mode.
- Interactive mode offers a service list, a log tail view, and
  keyboard navigation with visible key hints.
- Documents the CLI/TUI boundary in the project README (what triggers the
  TUI, what stays script-friendly).

## Fail Signals

- Forces the TUI on when stdout is a pipe, breaking CI.
- Drops or renames subcommands, or changes their output format.
- Replaces flags with interactive prompts only.
- No key hints; navigation undocumented.

## References Expected

- `references/architecture-patterns.md`
- `references/interaction-guide.md`
- `references/states-and-feedback.md`
- `frameworks/textual-python.md`

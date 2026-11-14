# Eval: Rendering — tmux Garbling, SSH Colors, Trashed Terminal

## Category

`rendering-troubleshooting`

## Prompt

My Ratatui log monitor looks fine in a bare terminal but garbles inside
tmux, colors are wrong over SSH, and when it panics my terminal is left
broken — I have to run `reset` every time. Resizing the window during a
burst of logs also freezes the UI for seconds. Fix all of it.

## Fixture

```rust
fn main() {
    let mut stdout = io::stdout();
    enable_raw_mode().unwrap();
    execute!(stdout, EnterAlternateScreen).unwrap();

    std::thread::spawn(|| {
        // network thread: draws directly on each incoming log line
        loop {
            let line = receive_log_line();
            draw_frame(&line, hardcoded_truecolor());
        }
    });
    read_keys(); // on panic or error: process just exits
}
```

## Pass Criteria

- Diagnoses by layer instead of guessing: emulator → multiplexer → SSH →
  app, and says which symptom belongs to which layer.
- Feature-detects at startup (`TERM`, `COLORTERM`, `TERM_PROGRAM`, `TMUX`)
  and degrades color truecolor → 256 → 16; no hardcoded truecolor.
- Restores the terminal on every exit path — panic hook plus a guard/defer
  covering EnterAlternateScreen, raw mode, and cursor state; no raw-mode
  leak.
- Moves rendering off the network thread: events feed state, a single
  render path draws, resizes are debounced/coalesced (~50ms), and log
  bursts get backpressure (bounded buffer with drop accounting) instead of
  per-line redraws.
- Documents which terminals/multiplexer combos are now supported and what
  still degrades.

## Fail Signals

- Advises "just run `reset`" or blames tmux without detection logic.
- Restores the terminal only on normal exit.
- Keeps per-line redraws from the producer thread.
- No debounce for resize; unbounded buffering.

## References Expected

- `references/troubleshooting.md`
- `references/terminal-compatibility.md`
- `references/stability-and-robustness.md`

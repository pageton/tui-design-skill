# Eval: RTL — Arabic Text in a Log Viewer

## Category

`rtl-bidi`

## Prompt

Our Cairo team says the log viewer is unusable with Arabic: when they paste
Arabic search terms the match highlighting lands on the wrong characters, and
Arabic log lines render scrambled. They also want the sidebar labels in
Arabic. Make Arabic work. (It's a Go Bubble Tea app.)

## Fixture

A viewer whose display code "fixes" Arabic by reversing it, and whose search
highlights by byte offsets:

```go
func displayLine(line string) string {
    if isArabic(line) {
        return reverse(line) // make it look right to left
    }
    return line
}

func highlight(line, query string) string {
    i := strings.Index(line, query)
    return line[:i] + "\x1b[7m" + line[i:i+len(query)] + "\x1b[0m" + line[i+len(query):]
}
```

## Pass Criteria

- Removes the manual reversal entirely: text is stored and passed in logical
  order; nothing mutates the string to look visually correct.
- Explains why: none of the four frameworks does BiDi; the terminal emulator
  (kitty, Ghostty, WezTerm, iTerm2, Windows Terminal) handles reordering,
  and pre-reversal breaks exactly those emulators.
- Localizes labels by right-aligning Arabic runs (direction detection for
  alignment only) — no reshaping, no digit transliteration, no punctuation
  "fixing".
- Search matches logical strings and highlights with display-width-safe
  spans (no byte slicing into the middle of a grapheme).
- Adds tests with Arabic, mixed Arabic/Latin lines, and Arabic+numbers; on
  non-BiDi terminals (e.g. Alacritty) documents the limitation instead of
  pretending support.

## Fail Signals

- Keeps or introduces reversal, or recommends an arabic-reshaper-style
  "fix" at display time.
- Transliterates digits or reorders punctuation manually.
- Claims the framework or app "does BiDi" without an emulator that does.
- Byte-offset highlighting left in place.

## References Expected

- `references/rtl-and-bidi.md`
- `references/unicode-and-text.md`
- `references/testing-tuis.md`

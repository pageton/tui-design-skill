# Eval: Unicode — Broken Table Alignment

## Category

`unicode`

## Prompt

The table in our Rust Ratatui app misaligns whenever a row contains CJK
filenames, emoji, or flag emojis — every column after the wide cell shifts
left or right. Fix the alignment. Rows can also contain combining characters
from usernames.

## Fixture

Column padding counts `char`s:

```rust
fn pad(s: &str, width: usize) -> String {
    let mut out = s.to_string();
    for _ in s.chars().count()..width {
        out.push(' ');
    }
    out
}

// usage: Row::new(vec![pad(name, 28), pad(size, 10), pad(modified, 19)])
```

## Pass Criteria

- Replaces char-count padding with display-width math (`unicode-width`):
  CJK counted as 2 cells, combining marks and ZWJ as 0, emoji sequences and
  flags measured as clusters.
- Truncates on grapheme-cluster boundaries with `…`, and pads/truncates
  before measuring — never truncating mid-cluster.
- Adds regression tests with: CJK filenames, an emoji-with-ZWJ sequence, a
  combining-mark username, a national flag, and mixed rows — asserted at
  fixed column widths, headless.
- Uses the width helper already in the dependency tree (Ratatui pulls a
  unicode-width crate) rather than adding a second width library.
- Checks other layout math in the file for the same bug class (len vs
  display width), not just the one function.

## Fail Signals

- Fixes only the reported function and leaves sibling len-based math.
- Strips diacritics or deletes combining marks to "shorten" text.
- Adds a second display-width dependency.
- Tests only ASCII, or no tests at all.

## References Expected

- `references/unicode-and-text.md`
- `references/testing-tuis.md`
- `references/component-catalog.md`

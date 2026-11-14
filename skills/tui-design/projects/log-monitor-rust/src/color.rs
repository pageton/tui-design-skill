//! Color tier detection — implements the ladder from
//! `references/terminal-compatibility.md` §3.
//!
//! Ratatui does not auto-downgrade colors: pick `Color::Rgb` vs
//! `Color::Indexed` from the detected tier and never emit above it.
//! `TMUX`/`TERM_PROGRAM` are consulted directly — the multiplexer is not
//! inferred from `TERM` alone (users override `TERM`).

use std::sync::OnceLock;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum ColorTier {
    Mono,
    TrueColor,
    Color256,
    Ansi16,
}

impl ColorTier {
    /// Detect once at startup from the environment; cached thereafter.
    pub fn detect() -> Self {
        Self::from_env(
            std::env::var("NO_COLOR").is_ok(),
            std::env::var("COLORTERM").ok().as_deref(),
            std::env::var("TERM").unwrap_or_default().as_str(),
            in_multiplexer(
                std::env::var("TMUX").is_ok(),
                std::env::var("TERM_PROGRAM").ok().as_deref(),
            ),
        )
    }

    /// The ladder, pure over its inputs (unit-tested):
    /// NO_COLOR → mono; inside a multiplexer only a forwarded COLORTERM
    /// grants truecolor; otherwise COLORTERM/`-direct` → truecolor;
    /// `256color` in TERM → 256; otherwise 16 ANSI colors.
    pub fn from_env(
        no_color: bool,
        colorterm: Option<&str>,
        term: &str,
        in_multiplexer: bool,
    ) -> Self {
        if no_color {
            return Self::Mono;
        }
        let forwarded_truecolor = matches!(colorterm, Some("truecolor") | Some("24bit"));
        let truecolor = if in_multiplexer {
            // tmux*/screen* TERM never implies 24-bit, and older tmux does
            // not pass -direct through: only the forwarded COLORTERM counts.
            forwarded_truecolor
        } else {
            forwarded_truecolor || term.ends_with("-direct")
        };
        if truecolor {
            Self::TrueColor
        } else if term.contains("256color") {
            Self::Color256
        } else {
            Self::Ansi16
        }
    }
}

fn in_multiplexer(tmux: bool, term_program: Option<&str>) -> bool {
    tmux || term_program == Some("tmux")
}

static TIER: OnceLock<ColorTier> = OnceLock::new();

/// The process-wide detected tier.
pub fn tier() -> ColorTier {
    *TIER.get_or_init(ColorTier::detect)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn no_color_policy_wins() {
        assert_eq!(
            ColorTier::from_env(true, Some("truecolor"), "xterm-256color", false),
            ColorTier::Mono
        );
    }

    #[test]
    fn colorterm_truecolor_and_24bit() {
        assert_eq!(
            ColorTier::from_env(false, Some("truecolor"), "xterm-256color", false),
            ColorTier::TrueColor
        );
        assert_eq!(
            ColorTier::from_env(false, Some("24bit"), "xterm-256color", false),
            ColorTier::TrueColor
        );
    }

    #[test]
    fn direct_term_is_truecolor_outside_tmux() {
        assert_eq!(
            ColorTier::from_env(false, None, "xterm-direct", false),
            ColorTier::TrueColor
        );
    }

    #[test]
    fn term_256color_is_the_middle_tier() {
        assert_eq!(
            ColorTier::from_env(false, None, "xterm-256color", false),
            ColorTier::Color256
        );
        // Inside tmux without COLORTERM forwarded: drop to 256, not 16.
        assert_eq!(
            ColorTier::from_env(false, None, "tmux-256color", true),
            ColorTier::Color256
        );
    }

    #[test]
    fn generic_term_is_16() {
        assert_eq!(
            ColorTier::from_env(false, None, "xterm", false),
            ColorTier::Ansi16
        );
        assert_eq!(
            ColorTier::from_env(false, None, "tmux", false),
            ColorTier::Ansi16
        );
    }

    #[test]
    fn unknown_colorterm_is_not_truecolor() {
        assert_eq!(
            ColorTier::from_env(false, Some("yes"), "xterm-256color", false),
            ColorTier::Color256
        );
    }

    #[test]
    fn tmux_never_implies_truecolor_from_term_alone() {
        // screen/tmux TERM without forwarded COLORTERM: never 24-bit.
        assert_eq!(
            ColorTier::from_env(false, None, "screen", true),
            ColorTier::Ansi16
        );
        // -direct is not trusted inside tmux (older tmux drops it).
        assert_eq!(
            ColorTier::from_env(false, None, "tmux-direct", true),
            ColorTier::Ansi16
        );
    }

    #[test]
    fn forwarded_colorterm_grants_truecolor_inside_tmux() {
        assert_eq!(
            ColorTier::from_env(false, Some("truecolor"), "screen-256color", true),
            ColorTier::TrueColor
        );
    }

    #[test]
    fn multiplexer_detection_uses_tmux_and_term_program() {
        assert!(in_multiplexer(true, None));
        assert!(in_multiplexer(false, Some("tmux")));
        assert!(!in_multiplexer(false, Some("iTerm.app")));
        assert!(!in_multiplexer(false, None));
    }

    #[test]
    fn term_program_tmux_affects_the_ladder() {
        // TERM overridden to a generic value, but TERM_PROGRAM=tmux:
        // COLORTERM is the only truecolor signal.
        assert_eq!(
            ColorTier::from_env(false, None, "xterm-256color", true),
            ColorTier::Color256
        );
        assert_eq!(
            ColorTier::from_env(false, Some("truecolor"), "xterm", true),
            ColorTier::TrueColor
        );
    }
}

//! re.sub, re.split and friends over fancy-regex, with Python's behavior where it differs. Shared by
//! the site crate and the bot.
use fancy_regex::{Captures, Regex, RegexBuilder};

pub fn rx(p: &str) -> Regex {
    RegexBuilder::new(p).backtrack_limit(100_000_000).build().unwrap_or_else(|e| panic!("{p}: {e}"))
}

#[macro_export]
macro_rules! re {
    ($p:expr) => {{
        static R: std::sync::LazyLock<fancy_regex::Regex> = std::sync::LazyLock::new(|| $crate::text::rx($p));
        &*R
    }};
}

pub fn caps<'t>(re: &Regex, text: &'t str) -> Option<Captures<'t, str>> {
    re.captures(text).expect("regex")
}

pub fn has(re: &Regex, text: &str) -> bool {
    re.is_match(text).expect("regex")
}

/// re.sub with a function for the replacement.
pub fn sub(re: &Regex, text: &str, mut f: impl FnMut(&Captures<'_, str>) -> String) -> String {
    let (mut out, mut last) = (String::with_capacity(text.len()), 0);
    for c in re.captures_iter(text) {
        let c = c.expect("regex");
        let m = c.get(0).unwrap();
        out.push_str(&text[last..m.start()]);
        out.push_str(&f(&c));
        last = m.end();
    }
    out.push_str(&text[last..]);
    out
}

/// re.split, without keeping the separators.
pub fn split<'t>(re: &Regex, text: &'t str) -> Vec<&'t str> {
    let (mut out, mut last) = (Vec::new(), 0);
    for m in re.find_iter(text) {
        let m = m.expect("regex");
        out.push(&text[last..m.start()]);
        last = m.end();
    }
    out.push(&text[last..]);
    out
}

/// A group's text, or "" when it did not take part.
pub fn group<'a>(c: &Captures<'a, str>, n: usize) -> &'a str {
    c.get(n).map_or("", |m| m.as_str())
}

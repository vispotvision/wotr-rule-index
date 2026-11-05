//! Python's number formats, as the embeds print them.

/// f"{n:,}"
pub fn commas(n: i64) -> String {
    group(&n.to_string())
}

/// f"{x:,.0f}"
pub fn commas0(x: f64) -> String {
    group(&format!("{x:.0}"))
}

fn group(s: &str) -> String {
    let (sign, digits) = s.strip_prefix('-').map_or(("", s), |d| ("-", d));
    let mut out = String::new();
    for (i, c) in digits.chars().enumerate() {
        if i > 0 && (digits.len() - i) % 3 == 0 {
            out.push(',');
        }
        out.push(c);
    }
    format!("{sign}{out}")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn thousands() {
        assert_eq!(commas(1234567), "1,234,567");
        assert_eq!(commas(-1234), "-1,234");
        assert_eq!(commas(999), "999");
        assert_eq!(commas0(1234.5), "1,234");
        assert_eq!(commas0(1235.5), "1,236");
    }
}

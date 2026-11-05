//! What the published art depends on Python for: its random number generator, so each page keeps
//! the plate and starfield it already has, plus the small string rules the pages were written under.
use crate::rng::Random;
use sha1::Digest;

/// Random(int(sha1(seed).hexdigest()[:12], 16))
pub fn from_sha1(seed: &str) -> Random {
    Random::from_be_bytes(&sha1::Sha1::digest(seed.as_bytes())[..6])
}

/// Random(str): the string and its SHA-512, read as one integer.
pub fn from_str_seed(seed: &str) -> Random {
    let mut bytes = seed.as_bytes().to_vec();
    bytes.extend_from_slice(&sha2::Sha512::digest(seed.as_bytes()));
    Random::from_be_bytes(&bytes)
}

/// hashlib.sha1(s).hexdigest()[:8]
pub fn sha8(s: &str) -> String {
    sha1::Sha1::digest(s.as_bytes()).iter().take(4).map(|b| format!("{b:02x}")).collect()
}

/// html.escape(s, quote=True)
pub fn escape(s: &str) -> String {
    s.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace('\'', "&#x27;")
}

/// str.title(), which capitalizes after any character that is not cased: an apostrophe too.
pub fn title_case(s: &str) -> String {
    let mut prev_cased = false;
    let mut out = String::new();
    for c in s.chars() {
        if prev_cased {
            out.extend(c.to_lowercase());
        } else {
            out.extend(c.to_uppercase());
        }
        prev_cased = c.is_lowercase() || c.is_uppercase();
    }
    out
}

/// The first n characters.
pub fn chars(s: &str, n: usize) -> &str {
    s.char_indices().nth(n).map_or(s, |(i, _)| &s[..i])
}

#[cfg(test)]
mod tests {
    use super::*;

    // The values below were printed by CPython's random and str.
    #[test]
    fn int_seed_matches_python() {
        let mut r = from_sha1("Start Here");
        assert_eq!(r.randint(-40, 40), -22);
        assert_eq!(r.uniform(0.0, 1200.0), 142.89442111457794);
        assert_eq!(r.choice(&[5, 6, 8, 10, 12]), 5);
        assert_eq!(r.random(), 0.38730717165566053);
        assert_eq!(r.sample(&(0..40).collect::<Vec<_>>(), 6), [37, 17, 34, 16, 25, 35]);
    }

    #[test]
    fn str_seed_matches_python() {
        let mut r = from_str_seed("abcd1234");
        assert_eq!(r.uniform(0.0, 900.5), 280.364085472377);
        assert_eq!(r.choice(&[0.6, 0.9, 1.3]), 0.9);
        assert_eq!(r.random(), 0.6408146551899327);
    }

    #[test]
    fn float_formats_match_python() {
        let got: Vec<String> = [0.5f64, 1.5, 2.5, 1006.5, 0.125, 2.675, -0.04].iter().map(|v| format!("{v:.0} {v:.1} {v:.2}")).collect();
        assert_eq!(got.join(" | "), "0 0.5 0.50 | 2 1.5 1.50 | 2 2.5 2.50 | 1006 1006.5 1006.50 | 0 0.1 0.12 | 3 2.7 2.67 | -0 -0.0 -0.04");
    }

    #[test]
    fn title_breaks_on_an_apostrophe() {
        assert_eq!(title_case("THE MEASURE'S GOLD · A-B 3RD"), "The Measure'S Gold · A-B 3Rd");
    }
}

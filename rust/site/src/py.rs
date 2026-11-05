//! What the published art depends on Python for: its random number generator, so each page keeps
//! the plate and starfield it already has, plus the small string rules the pages were written under.
use fancy_regex::{Captures, Regex, RegexBuilder};
use sha1::Digest;

/// random.Random: MT19937 with Python's seeding and its derived draws.
pub struct Random {
    mt: [u32; 624],
    i: usize,
}

impl Random {
    fn from_key(key: &[u32]) -> Self {
        let mut mt = [0u32; 624];
        mt[0] = 19650218;
        for i in 1..624 {
            mt[i] = 1812433253u32.wrapping_mul(mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_add(i as u32);
        }
        let (mut i, mut j) = (1, 0);
        for _ in 0..624.max(key.len()) {
            mt[i] = (mt[i] ^ (mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_mul(1664525)).wrapping_add(key[j]).wrapping_add(j as u32);
            i += 1;
            j += 1;
            if i >= 624 {
                mt[0] = mt[623];
                i = 1;
            }
            if j >= key.len() {
                j = 0;
            }
        }
        for _ in 0..623 {
            mt[i] = (mt[i] ^ (mt[i - 1] ^ (mt[i - 1] >> 30)).wrapping_mul(1566083941)).wrapping_sub(i as u32);
            i += 1;
            if i >= 624 {
                mt[0] = mt[623];
                i = 1;
            }
        }
        mt[0] = 0x8000_0000;
        Random { mt, i: 624 }
    }

    /// Random(a big-endian integer): its 32-bit words, least significant first.
    fn from_be_bytes(be: &[u8]) -> Self {
        let mut key: Vec<u32> = be.rchunks(4).map(|c| c.iter().fold(0u32, |a, b| (a << 8) | u32::from(*b))).collect();
        while key.len() > 1 && key.last() == Some(&0) {
            key.pop();
        }
        Self::from_key(&key)
    }

    /// Random(int(sha1(seed).hexdigest()[:12], 16))
    pub fn from_sha1(seed: &str) -> Self {
        let d = sha1::Sha1::digest(seed.as_bytes());
        Self::from_be_bytes(&d[..6])
    }

    /// Random(str): the string and its SHA-512, read as one integer.
    pub fn from_str_seed(seed: &str) -> Self {
        let mut bytes = seed.as_bytes().to_vec();
        bytes.extend_from_slice(&sha2::Sha512::digest(seed.as_bytes()));
        Self::from_be_bytes(&bytes)
    }

    fn next_u32(&mut self) -> u32 {
        if self.i >= 624 {
            for k in 0..624 {
                let y = (self.mt[k] & 0x8000_0000) | (self.mt[(k + 1) % 624] & 0x7fff_ffff);
                self.mt[k] = self.mt[(k + 397) % 624] ^ (y >> 1) ^ if y & 1 == 1 { 0x9908_b0df } else { 0 };
            }
            self.i = 0;
        }
        let mut y = self.mt[self.i];
        self.i += 1;
        y ^= y >> 11;
        y ^= (y << 7) & 0x9d2c_5680;
        y ^= (y << 15) & 0xefc6_0000;
        y ^ (y >> 18)
    }

    pub fn random(&mut self) -> f64 {
        let (a, b) = (self.next_u32() >> 5, self.next_u32() >> 6);
        (f64::from(a) * 67108864.0 + f64::from(b)) / 9007199254740992.0
    }

    pub fn uniform(&mut self, a: f64, b: f64) -> f64 {
        a + (b - a) * self.random()
    }

    pub fn below(&mut self, n: u32) -> u32 {
        let k = 32 - n.leading_zeros();
        loop {
            let r = self.next_u32() >> (32 - k);
            if r < n {
                return r;
            }
        }
    }

    pub fn randint(&mut self, a: i64, b: i64) -> i64 {
        a + i64::from(self.below((b - a + 1) as u32))
    }

    pub fn choice<T: Copy>(&mut self, items: &[T]) -> T {
        items[self.below(items.len() as u32) as usize]
    }

    /// random.sample for a small k out of a small population (its pool branch).
    pub fn sample<T: Copy>(&mut self, items: &[T], k: usize) -> Vec<T> {
        let mut pool = items.to_vec();
        let n = pool.len();
        (0..k)
            .map(|i| {
                let j = self.below((n - i) as u32) as usize;
                let v = pool[j];
                pool[j] = pool[n - i - 1];
                v
            })
            .collect()
    }
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

pub fn rx(p: &str) -> Regex {
    RegexBuilder::new(p).backtrack_limit(100_000_000).build().unwrap_or_else(|e| panic!("{p}: {e}"))
}

#[macro_export]
macro_rules! re {
    ($p:expr) => {{
        static R: std::sync::LazyLock<fancy_regex::Regex> = std::sync::LazyLock::new(|| $crate::py::rx($p));
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

#[cfg(test)]
mod tests {
    use super::*;

    // The values below were printed by CPython's random and str.
    #[test]
    fn int_seed_matches_python() {
        let mut r = Random::from_sha1("Start Here");
        assert_eq!(r.randint(-40, 40), -22);
        assert_eq!(r.uniform(0.0, 1200.0), 142.89442111457794);
        assert_eq!(r.choice(&[5, 6, 8, 10, 12]), 5);
        assert_eq!(r.random(), 0.38730717165566053);
        assert_eq!(r.sample(&(0..40).collect::<Vec<_>>(), 6), [37, 17, 34, 16, 25, 35]);
    }

    #[test]
    fn str_seed_matches_python() {
        let mut r = Random::from_str_seed("abcd1234");
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

//! Python's json module where its exact behavior shows in a reply: json.loads with its error text
//! ("Expecting ',' delimiter: line 1 column 9 (char 8)", positions in code points; the string
//! errors are the C scanner's, the default), and json.dumps(v, indent=N) with ensure_ascii.
use serde_json::{Map, Number, Value};

enum J {
    Stop(usize),
    Err(String),
}

struct P<'a> {
    s: &'a [char],
}

impl P<'_> {
    fn err(&self, msg: &str, pos: usize) -> J {
        let before = &self.s[..pos.min(self.s.len())];
        let line = before.iter().filter(|c| **c == '\n').count() + 1;
        let col = pos as i64 - before.iter().rposition(|c| *c == '\n').map_or(-1, |i| i as i64);
        J::Err(format!("{msg}: line {line} column {col} (char {pos})"))
    }

    fn at(&self, i: usize) -> Option<char> {
        self.s.get(i).copied()
    }

    fn ws(&self, mut i: usize) -> usize {
        while matches!(self.at(i), Some(' ' | '\t' | '\n' | '\r')) {
            i += 1;
        }
        i
    }

    fn lit(&self, i: usize, w: &str) -> bool {
        w.chars().enumerate().all(|(k, c)| self.at(i + k) == Some(c))
    }

    fn scan(&self, i: usize) -> Result<(Value, usize), J> {
        let Some(c) = self.at(i) else { return Err(J::Stop(i)) };
        match c {
            '"' => return self.string(i + 1).map(|(t, e)| (Value::String(t), e)),
            '{' => return self.object(i + 1),
            '[' => return self.array(i + 1),
            'n' if self.lit(i, "null") => return Ok((Value::Null, i + 4)),
            't' if self.lit(i, "true") => return Ok((Value::Bool(true), i + 4)),
            'f' if self.lit(i, "false") => return Ok((Value::Bool(false), i + 5)),
            _ => {}
        }
        if let Some(r) = self.number(i) {
            return Ok(r);
        }
        // NaN and the infinities have no JSON value: their str() stands in, truthy as the floats are
        for (w, v) in [("NaN", "nan"), ("Infinity", "inf"), ("-Infinity", "-inf")] {
            if self.lit(i, w) {
                return Ok((Value::String(v.into()), i + w.chars().count()));
            }
        }
        Err(J::Stop(i))
    }

    /// NUMBER_RE: (-?(?:0|[1-9][0-9]*))(\.[0-9]+)?([eE][-+]?[0-9]+)?
    fn number(&self, i: usize) -> Option<(Value, usize)> {
        let digit = |k: usize| self.at(k).is_some_and(|c| c.is_ascii_digit());
        let mut k = i + usize::from(self.at(i) == Some('-'));
        match self.at(k) {
            Some('0') => k += 1,
            Some('1'..='9') => {
                while digit(k) {
                    k += 1;
                }
            }
            _ => return None,
        }
        let mut float = false;
        if self.at(k) == Some('.') && digit(k + 1) {
            k += 1;
            while digit(k) {
                k += 1;
            }
            float = true;
        }
        if matches!(self.at(k), Some('e' | 'E')) {
            let mut e = k + 1;
            if matches!(self.at(e), Some('-' | '+')) {
                e += 1;
            }
            if digit(e) {
                while digit(e) {
                    e += 1;
                }
                k = e;
                float = true;
            }
        }
        let text: String = self.s[i..k].iter().collect();
        let f = || text.parse::<f64>().unwrap_or(f64::NAN);
        let n = if float { None } else { text.parse::<i64>().map(Number::from).or_else(|_| text.parse::<u64>().map(Number::from)).ok() };
        let v = n.or_else(|| Number::from_f64(f())).map_or_else(|| Value::String(if f() > 0.0 { "inf" } else { "-inf" }.into()), Value::Number);
        Some((v, k))
    }

    /// _json.c scanstring_unicode; `end` is just past the opening quote.
    fn string(&self, end: usize) -> Result<(String, usize), J> {
        let (begin, len) = (end - 1, self.s.len());
        let mut out = String::new();
        let mut end = end;
        loop {
            let mut next = end;
            while next < len && !matches!(self.s[next], '"' | '\\') {
                if (self.s[next] as u32) <= 0x1f {
                    return Err(self.err("Invalid control character at", next));
                }
                next += 1;
            }
            if next == len {
                return Err(self.err("Unterminated string starting at", begin));
            }
            out.extend(&self.s[end..next]);
            if self.s[next] == '"' {
                return Ok((out, next + 1));
            }
            next += 1;
            if next == len {
                return Err(self.err("Unterminated string starting at", begin));
            }
            let c = self.s[next];
            if c != 'u' {
                end = next + 1;
                out.push(match c {
                    '"' => '"',
                    '\\' => '\\',
                    '/' => '/',
                    'b' => '\u{8}',
                    'f' => '\u{c}',
                    'n' => '\n',
                    'r' => '\r',
                    't' => '\t',
                    _ => return Err(self.err("Invalid \\escape", end - 2)),
                });
                continue;
            }
            next += 1;
            end = next + 4;
            if end >= len {
                return Err(self.err("Invalid \\uXXXX escape", next - 1));
            }
            let hex = |from: usize| -> Option<u32> { self.s[from..from + 4].iter().try_fold(0, |a, c| c.to_digit(16).map(|d| a << 4 | d)) };
            let Some(mut u) = hex(next) else { return Err(self.err("Invalid \\uXXXX escape", end - 5)) };
            if (0xd800..=0xdbff).contains(&u) && end + 6 < len && self.s[end] == '\\' && self.s[end + 1] == 'u' {
                let Some(u2) = hex(end + 2) else { return Err(self.err("Invalid \\uXXXX escape", end + 1)) };
                if (0xdc00..=0xdfff).contains(&u2) {
                    u = 0x10000 + ((u - 0xd800) << 10 | (u2 - 0xdc00));
                    end += 6;
                }
            }
            out.push(char::from_u32(u).unwrap_or('\u{fffd}')); // a lone surrogate has no char
        }
    }

    /// decoder.JSONObject; `end` is just past the '{'.
    fn object(&self, mut end: usize) -> Result<(Value, usize), J> {
        let mut m = Map::new();
        let mut next = self.at(end);
        if next != Some('"') {
            end = self.ws(end);
            next = self.at(end);
            if next == Some('}') {
                return Ok((Value::Object(m), end + 1));
            }
            if next != Some('"') {
                return Err(self.err("Expecting property name enclosed in double quotes", end));
            }
        }
        end += 1;
        loop {
            let (key, e) = self.string(end)?;
            end = e;
            if self.at(end) != Some(':') {
                end = self.ws(end);
                if self.at(end) != Some(':') {
                    return Err(self.err("Expecting ':' delimiter", end));
                }
            }
            end = self.ws(end + 1);
            let (v, e) = self.scan(end).map_err(|j| match j {
                J::Stop(i) => self.err("Expecting value", i),
                e => e,
            })?;
            m.insert(key, v);
            end = self.ws(e);
            let next = self.at(end);
            end += 1;
            match next {
                Some('}') => return Ok((Value::Object(m), end)),
                Some(',') => {}
                _ => return Err(self.err("Expecting ',' delimiter", end - 1)),
            }
            let comma = end - 1;
            end = self.ws(end);
            let next = self.at(end);
            end += 1;
            if next != Some('"') {
                if next == Some('}') {
                    return Err(self.err("Illegal trailing comma before end of object", comma));
                }
                return Err(self.err("Expecting property name enclosed in double quotes", end - 1));
            }
        }
    }

    /// decoder.JSONArray; `end` is just past the '['.
    fn array(&self, mut end: usize) -> Result<(Value, usize), J> {
        let mut out = Vec::new();
        end = self.ws(end);
        if self.at(end) == Some(']') {
            return Ok((Value::Array(out), end + 1));
        }
        loop {
            let (v, e) = self.scan(end).map_err(|j| match j {
                J::Stop(i) => self.err("Expecting value", i),
                e => e,
            })?;
            out.push(v);
            end = self.ws(e);
            let next = self.at(end);
            end += 1;
            match next {
                Some(']') => return Ok((Value::Array(out), end)),
                Some(',') => {}
                _ => return Err(self.err("Expecting ',' delimiter", end - 1)),
            }
            let comma = end - 1;
            end = self.ws(end);
            if self.at(end) == Some(']') {
                return Err(self.err("Illegal trailing comma before end of array", comma));
            }
        }
    }
}

/// json.loads(s); the error is str(JSONDecodeError).
pub fn loads(s: &str) -> Result<Value, String> {
    let c: Vec<char> = s.chars().collect();
    let p = P { s: &c };
    if c.first() == Some(&'\u{feff}') {
        return Err("Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)".into());
    }
    let r = p.scan(p.ws(0)).and_then(|(v, end)| {
        let end = p.ws(end);
        if end != c.len() { Err(p.err("Extra data", end)) } else { Ok(v) }
    });
    r.map_err(|j| match j {
        J::Stop(i) => match p.err("Expecting value", i) {
            J::Err(m) => m,
            J::Stop(_) => unreachable!(),
        },
        J::Err(m) => m,
    })
}

fn ascii_str(t: &str, out: &mut String) {
    out.push('"');
    for c in t.chars() {
        match c {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            '\u{8}' => out.push_str("\\b"),
            '\u{c}' => out.push_str("\\f"),
            ' '..='~' => out.push(c),
            c => {
                let mut b = [0u16; 2];
                for u in c.encode_utf16(&mut b) {
                    out.push_str(&format!("\\u{u:04x}"));
                }
            }
        }
    }
    out.push('"');
}

/// json.dumps(v, sort_keys=sort_keys): ensure_ascii, ", " and ": " separators.
pub fn dumps(v: &Value, sort_keys: bool) -> String {
    fn go(v: &Value, sort: bool, out: &mut String) {
        match v {
            Value::Array(a) => {
                out.push('[');
                for (i, x) in a.iter().enumerate() {
                    out.push_str(if i > 0 { ", " } else { "" });
                    go(x, sort, out);
                }
                out.push(']');
            }
            Value::Object(o) => {
                let mut keys: Vec<&String> = o.keys().collect();
                if sort {
                    keys.sort();
                }
                out.push('{');
                for (i, k) in keys.into_iter().enumerate() {
                    out.push_str(if i > 0 { ", " } else { "" });
                    ascii_str(k, out);
                    out.push_str(": ");
                    go(&o[k], sort, out);
                }
                out.push('}');
            }
            Value::String(t) => ascii_str(t, out),
            o => out.push_str(&o.to_string()),
        }
    }
    let mut out = String::new();
    go(v, sort_keys, &mut out);
    out
}

/// json.dumps(v, indent=indent): ensure_ascii, "," and ": " separators.
pub fn dumps_indent(v: &Value, indent: usize) -> String {
    fn go(v: &Value, indent: usize, level: usize, out: &mut String) {
        let pad = |l: usize| format!("\n{}", " ".repeat(indent * l));
        match v {
            Value::Array(a) if !a.is_empty() => {
                out.push('[');
                for (i, x) in a.iter().enumerate() {
                    out.push_str(if i > 0 { "," } else { "" });
                    out.push_str(&pad(level + 1));
                    go(x, indent, level + 1, out);
                }
                out.push_str(&pad(level));
                out.push(']');
            }
            Value::Object(o) if !o.is_empty() => {
                out.push('{');
                for (i, (k, x)) in o.iter().enumerate() {
                    out.push_str(if i > 0 { "," } else { "" });
                    out.push_str(&pad(level + 1));
                    ascii_str(k, out);
                    out.push_str(": ");
                    go(x, indent, level + 1, out);
                }
                out.push_str(&pad(level));
                out.push('}');
            }
            Value::String(t) => ascii_str(t, out),
            o => out.push_str(&o.to_string()),
        }
    }
    let mut out = String::new();
    go(v, indent, 0, &mut out);
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn python_messages() {
        for (doc, want) in [
            ("{\"a\": \"x\ty\"}", "Invalid control character at: line 1 column 9 (char 8)"),
            ("{\"a\": \"\\q\"}", "Invalid \\escape: line 1 column 8 (char 7)"),
            ("{\"a\": 1,}", "Illegal trailing comma before end of object: line 1 column 8 (char 7)"),
            ("[1,]", "Illegal trailing comma before end of array: line 1 column 3 (char 2)"),
            ("{\"a\": 01}", "Expecting ',' delimiter: line 1 column 8 (char 7)"),
            ("{\"a\":\n\n 1 2}", "Expecting ',' delimiter: line 3 column 4 (char 10)"),
            ("{\"a\": 1} x", "Extra data: line 1 column 10 (char 9)"),
            ("{\"a\": \"unterminated", "Unterminated string starting at: line 1 column 7 (char 6)"),
            ("", "Expecting value: line 1 column 1 (char 0)"),
        ] {
            assert_eq!(loads(doc).unwrap_err(), want, "{doc:?}");
        }
        assert_eq!(loads(" {\"é\": [1, 2.5, \"\\u00e9\\ud83d\\ude00\"], \"b\": {}} ").unwrap(), serde_json::json!({"é": [1, 2.5, "é😀"], "b": {}}));
        assert_eq!(dumps_indent(&serde_json::json!([{"a": "é\u{7f}", "b": [], "c": 3}]), 1), "[\n {\n  \"a\": \"\\u00e9\\u007f\",\n  \"b\": [],\n  \"c\": 3\n }\n]");
    }
}

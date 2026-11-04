//! `yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=100)`, byte for byte: a port of
//! PyYAML's Emitter (block style, scalar analysis, the plain/single/double-quoted writers and their
//! line folding), its YAML 1.1 implicit resolver and its float representer. table/*.yaml is this
//! format; the Rust writers must not reformat it. Checked against PyYAML by rust/yaml_parity.py.
//! ponytail: no anchors/aliases (the table never shares an object between rows) and no folded or
//! literal block scalars (safe_dump never chooses them).
use serde_json::Value;
use std::sync::LazyLock;

const WIDTH: usize = 100;
const INDENT: usize = 2;
const BREAKS: [char; 4] = ['\n', '\u{85}', '\u{2028}', '\u{2029}'];
const WS: [char; 8] = ['\0', ' ', '\t', '\r', '\n', '\u{85}', '\u{2028}', '\u{2029}'];

static RESOLVERS: LazyLock<Vec<(&'static str, &'static str, regex::Regex)>> = LazyLock::new(|| {
    // (first characters, tag, the regex with Python's `$`, which also matches before a final newline)
    [
        ("yYnNtTfFoO", "bool", r"^(?:yes|Yes|YES|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF)\n?\z"),
        ("-+0123456789.", "float", r"^(?:[-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?|\.[0-9][0-9_]*(?:[eE][-+][0-9]+)?|[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\.[0-9_]*|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))\n?\z"),
        ("-+0123456789", "int", r"^(?:[-+]?0b[0-1_]+|[-+]?0[0-7_]+|[-+]?(?:0|[1-9][0-9_]*)|[-+]?0x[0-9a-fA-F_]+|[-+]?[1-9][0-9_]*(?::[0-5]?[0-9])+)\n?\z"),
        ("<", "merge", r"^(?:<<)\n?\z"),
        ("~nN", "null", r"^(?:~|null|Null|NULL|)\n?\z"),
        ("0123456789", "timestamp", r"^(?:[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]|[0-9][0-9][0-9][0-9]-[0-9][0-9]?-[0-9][0-9]?(?:[Tt]|[ \t]+)[0-9][0-9]?:[0-9][0-9]:[0-9][0-9](?:\.[0-9]*)?(?:[ \t]*(?:Z|[-+][0-9][0-9]?(?::[0-9][0-9])?))?)\n?\z"),
        ("=", "value", r"^(?:=)\n?\z"),
        ("!&*", "yaml", r"^(?:!|&|\*)\n?\z"),
    ]
    .into_iter()
    .map(|(f, t, r)| (f, t, regex::Regex::new(r).unwrap()))
    .collect()
});

/// Would this text, written plain, read back as something other than a string?
fn resolves_non_str(v: &str) -> bool {
    let first = v.chars().next();
    RESOLVERS.iter().any(|(chars, _, r)| match first {
        None => chars.contains('n') && r.is_match(""), // only null registers the empty string
        Some(c) => chars.contains(c) && r.is_match(v),
    })
}

/// Python's repr() of a float, then PyYAML's representer fix-ups.
fn float_repr(f: f64) -> String {
    if f.is_nan() {
        return ".nan".into();
    }
    if f.is_infinite() {
        return if f > 0.0 { ".inf" } else { "-.inf" }.into();
    }
    // shortest round-trip digits, formatted as Python's repr: fixed for -4 <= exp < 16
    let e = format!("{:e}", f.abs());
    let (mant, exp) = e.split_once('e').unwrap();
    let exp: i32 = exp.parse().unwrap();
    let digits: String = mant.chars().filter(|c| *c != '.').collect();
    let sign = if f.is_sign_negative() { "-" } else { "" };
    let s = if (-4..16).contains(&exp) {
        if exp >= 0 {
            let int_len = exp as usize + 1;
            if digits.len() <= int_len {
                format!("{}{}.0", digits, "0".repeat(int_len - digits.len()))
            } else {
                format!("{}.{}", &digits[..int_len], &digits[int_len..])
            }
        } else {
            format!("0.{}{}", "0".repeat((-exp - 1) as usize), digits)
        }
    } else {
        let m = if digits.len() > 1 { format!("{}.{}", &digits[..1], &digits[1..]) } else { digits.clone() };
        format!("{m}e{}{:02}", if exp < 0 { "-" } else { "+" }, exp.abs())
    };
    let mut v = format!("{sign}{s}").to_lowercase();
    if !v.contains('.') && v.contains('e') {
        v = v.replacen('e', ".0e", 1);
    }
    v
}

struct Analysis {
    empty: bool,
    multiline: bool,
    allow_flow_plain: bool,
    allow_block_plain: bool,
    allow_single_quoted: bool,
}

fn analyze(s: &[char]) -> Analysis {
    if s.is_empty() {
        return Analysis { empty: true, multiline: false, allow_flow_plain: false, allow_block_plain: true, allow_single_quoted: true };
    }
    let (mut block_ind, mut flow_ind, mut line_breaks, mut special) = (false, false, false, false);
    let (mut lead_sp, mut lead_br, mut trail_sp, mut trail_br, mut break_space, mut space_break) = (false, false, false, false, false, false);
    let starts = |p: &str| s.iter().take(3).collect::<String>() == p;
    if starts("---") || starts("...") {
        block_ind = true;
        flow_ind = true;
    }
    let mut preceded_ws = true;
    let mut followed_ws = s.len() == 1 || WS.contains(&s[1]);
    let (mut prev_space, mut prev_break) = (false, false);
    let n = s.len();
    for (i, &ch) in s.iter().enumerate() {
        if i == 0 {
            if "#,[]{}&*!|>'\"%@`".contains(ch) {
                flow_ind = true;
                block_ind = true;
            }
            if "?:".contains(ch) {
                flow_ind = true;
                if followed_ws {
                    block_ind = true;
                }
            }
            if ch == '-' && followed_ws {
                flow_ind = true;
                block_ind = true;
            }
        } else {
            if ",?[]{}".contains(ch) {
                flow_ind = true;
            }
            if ch == ':' {
                flow_ind = true;
                if followed_ws {
                    block_ind = true;
                }
            }
            if ch == '#' && preceded_ws {
                flow_ind = true;
                block_ind = true;
            }
        }
        if BREAKS.contains(&ch) {
            line_breaks = true;
        }
        let c = ch as u32;
        if !(ch == '\n' || (0x20..=0x7E).contains(&c)) {
            let unicode = (ch == '\u{85}' || (0xA0..=0xD7FF).contains(&c) || (0xE000..=0xFFFD).contains(&c) || (0x10000..0x10FFFF).contains(&c)) && ch != '\u{FEFF}';
            if !unicode {
                special = true; // allow_unicode=True: unicode characters are fine
            }
        }
        if ch == ' ' {
            if i == 0 {
                lead_sp = true;
            }
            if i == n - 1 {
                trail_sp = true;
            }
            if prev_break {
                break_space = true;
            }
            prev_space = true;
            prev_break = false;
        } else if BREAKS.contains(&ch) {
            if i == 0 {
                lead_br = true;
            }
            if i == n - 1 {
                trail_br = true;
            }
            if prev_space {
                space_break = true;
            }
            prev_space = false;
            prev_break = true;
        } else {
            prev_space = false;
            prev_break = false;
        }
        preceded_ws = WS.contains(&ch);
        followed_ws = i + 2 >= n || WS.contains(&s[i + 2]);
    }
    let (mut afp, mut abp, mut asq) = (true, true, true);
    if lead_sp || lead_br || trail_sp || trail_br {
        afp = false;
        abp = false;
    }
    if break_space {
        afp = false;
        abp = false;
        asq = false;
    }
    if space_break || special {
        afp = false;
        abp = false;
        asq = false;
    }
    if line_breaks {
        afp = false;
        abp = false;
    }
    if flow_ind {
        afp = false;
    }
    if block_ind {
        abp = false;
    }
    Analysis { empty: false, multiline: line_breaks, allow_flow_plain: afp, allow_block_plain: abp, allow_single_quoted: asq }
}

#[derive(Default)]
struct Emitter {
    out: String,
    indents: Vec<Option<usize>>,
    indent: Option<usize>,
    flow_level: usize,
    root_context: bool,
    mapping_context: bool,
    simple_key_context: bool,
    column: usize,
    whitespace: bool,
    indention: bool,
    open_ended: bool,
}

impl Emitter {
    fn increase_indent(&mut self, flow: bool, indentless: bool) {
        self.indents.push(self.indent);
        match self.indent {
            None => self.indent = Some(if flow { INDENT } else { 0 }),
            Some(i) if !indentless => self.indent = Some(i + INDENT),
            _ => {}
        }
    }

    fn pop_indent(&mut self) {
        self.indent = self.indents.pop().unwrap();
    }

    fn write(&mut self, data: &str) {
        self.column += data.chars().count();
        self.out.push_str(data);
    }

    fn write_indicator(&mut self, ind: &str, need_ws: bool, whitespace: bool, indention: bool) {
        let data = if self.whitespace || !need_ws { ind.to_string() } else { format!(" {ind}") };
        self.whitespace = whitespace;
        self.indention = self.indention && indention;
        self.open_ended = false;
        self.write(&data);
    }

    fn write_indent(&mut self) {
        let indent = self.indent.unwrap_or(0);
        if !self.indention || self.column > indent || (self.column == indent && !self.whitespace) {
            self.write_line_break(None);
        }
        if self.column < indent {
            self.whitespace = true;
            let pad = " ".repeat(indent - self.column);
            self.out.push_str(&pad);
            self.column = indent;
        }
    }

    fn write_line_break(&mut self, data: Option<char>) {
        self.whitespace = true;
        self.indention = true;
        self.column = 0;
        self.out.push(data.unwrap_or('\n'));
    }

    fn node(&mut self, v: &Value, root: bool, mapping: bool, simple_key: bool) {
        self.root_context = root;
        self.mapping_context = mapping;
        self.simple_key_context = simple_key;
        match v {
            Value::Array(a) if self.flow_level > 0 || a.is_empty() => self.flow_empty("[", "]"),
            Value::Object(o) if self.flow_level > 0 || o.is_empty() => self.flow_empty("{", "}"),
            Value::Array(a) => {
                let indentless = self.mapping_context && !self.indention;
                self.increase_indent(false, indentless);
                for item in a {
                    self.write_indent();
                    self.write_indicator("-", true, false, true);
                    self.node(item, false, false, false);
                }
                self.pop_indent();
            }
            Value::Object(o) => {
                self.increase_indent(false, false);
                for (k, val) in o {
                    self.write_indent();
                    let key = Value::String(k.clone());
                    if self.check_simple_key(k) {
                        self.node(&key, false, true, true);
                        self.write_indicator(":", false, false, false);
                    } else {
                        self.write_indicator("?", true, false, true);
                        self.node(&key, false, true, false);
                        self.write_indent();
                        self.write_indicator(":", true, false, true);
                    }
                    self.node(val, false, true, false);
                }
                self.pop_indent();
            }
            scalar => {
                self.increase_indent(true, false);
                self.scalar(scalar);
                self.pop_indent();
            }
        }
    }

    /// Only empty collections are ever flow style here (default_flow_style=False).
    fn flow_empty(&mut self, open: &str, close: &str) {
        self.write_indicator(open, true, true, false);
        self.flow_level += 1;
        self.increase_indent(true, false);
        self.pop_indent();
        self.flow_level -= 1;
        self.write_indicator(close, false, false, false);
    }

    fn check_simple_key(&self, k: &str) -> bool {
        let chars: Vec<char> = k.chars().collect();
        let a = analyze(&chars);
        // the serializer tags every scalar; prepare_tag("tag:yaml.org,2002:str") is "!!str"
        chars.len() + "!!str".len() < 128 && !a.empty && !a.multiline
    }

    fn scalar(&mut self, v: &Value) {
        let (text, implicit_plain) = match v {
            Value::Null => ("null".to_string(), true),
            Value::Bool(b) => (if *b { "true" } else { "false" }.to_string(), true),
            Value::Number(n) if n.is_i64() || n.is_u64() => (n.to_string(), true),
            Value::Number(n) => (float_repr(n.as_f64().unwrap()), true),
            Value::String(s) => (s.clone(), !resolves_non_str(s)),
            _ => unreachable!(),
        };
        let chars: Vec<char> = text.chars().collect();
        let a = analyze(&chars);
        let plain_ok = implicit_plain
            && !(self.simple_key_context && (a.empty || a.multiline))
            && ((self.flow_level > 0 && a.allow_flow_plain) || (self.flow_level == 0 && a.allow_block_plain));
        let split = !self.simple_key_context;
        if plain_ok {
            self.write_plain(&chars, split);
        } else if a.allow_single_quoted && !(self.simple_key_context && a.multiline) {
            self.write_single_quoted(&chars, split);
        } else {
            self.write_double_quoted(&chars, split);
        }
    }

    fn write_plain(&mut self, t: &[char], split: bool) {
        if self.root_context {
            self.open_ended = true;
        }
        if t.is_empty() {
            return;
        }
        if !self.whitespace {
            self.write(" ");
        }
        self.whitespace = false;
        self.indention = false;
        let (mut spaces, mut breaks) = (false, false);
        let (mut start, mut end) = (0, 0);
        while end <= t.len() {
            let ch = t.get(end).copied();
            if spaces {
                if ch != Some(' ') {
                    if start + 1 == end && self.column > WIDTH && split {
                        self.write_indent();
                        self.whitespace = false;
                        self.indention = false;
                    } else {
                        let d: String = t[start..end].iter().collect();
                        self.write(&d);
                    }
                    start = end;
                }
            } else if breaks {
                if ch.is_none_or(|c| !BREAKS.contains(&c)) {
                    if t[start] == '\n' {
                        self.write_line_break(None);
                    }
                    for &br in &t[start..end] {
                        self.write_line_break(Some(br));
                    }
                    self.write_indent();
                    self.whitespace = false;
                    self.indention = false;
                    start = end;
                }
            } else if ch.is_none_or(|c| c == ' ' || BREAKS.contains(&c)) {
                let d: String = t[start..end].iter().collect();
                self.write(&d);
                start = end;
            }
            if let Some(c) = ch {
                spaces = c == ' ';
                breaks = BREAKS.contains(&c);
            }
            end += 1;
        }
    }

    fn write_single_quoted(&mut self, t: &[char], split: bool) {
        self.write_indicator("'", true, false, false);
        let (mut spaces, mut breaks) = (false, false);
        let (mut start, mut end) = (0, 0);
        while end <= t.len() {
            let ch = t.get(end).copied();
            if spaces {
                if ch != Some(' ') {
                    if start + 1 == end && self.column > WIDTH && split && start != 0 && end != t.len() {
                        self.write_indent();
                    } else {
                        let d: String = t[start..end].iter().collect();
                        self.write(&d);
                    }
                    start = end;
                }
            } else if breaks {
                if ch.is_none_or(|c| !BREAKS.contains(&c)) {
                    if t[start] == '\n' {
                        self.write_line_break(None);
                    }
                    for &br in &t[start..end] {
                        self.write_line_break(Some(br));
                    }
                    self.write_indent();
                    start = end;
                }
            } else if ch.is_none_or(|c| c == ' ' || BREAKS.contains(&c) || c == '\'') && start < end {
                let d: String = t[start..end].iter().collect();
                self.write(&d);
                start = end;
            }
            if ch == Some('\'') {
                self.write("''");
                start = end + 1;
            }
            if let Some(c) = ch {
                spaces = c == ' ';
                breaks = BREAKS.contains(&c);
            }
            end += 1;
        }
        self.write_indicator("'", false, false, false);
    }

    fn write_double_quoted(&mut self, t: &[char], split: bool) {
        self.write_indicator("\"", true, false, false);
        let (mut start, mut end) = (0, 0);
        while end <= t.len() {
            let ch = t.get(end).copied();
            let printable = |c: char| {
                let u = c as u32;
                (0x20..=0x7E).contains(&u) || (0xA0..=0xD7FF).contains(&u) || (0xE000..=0xFFFD).contains(&u)
            };
            if ch.is_none_or(|c| "\"\\\u{85}\u{2028}\u{2029}\u{FEFF}".contains(c) || !printable(c)) {
                if start < end {
                    let d: String = t[start..end].iter().collect();
                    self.write(&d);
                    start = end;
                }
                if let Some(c) = ch {
                    let esc = match c {
                        '\0' => "0".into(),
                        '\u{07}' => "a".into(),
                        '\u{08}' => "b".into(),
                        '\t' => "t".into(),
                        '\n' => "n".into(),
                        '\u{0B}' => "v".into(),
                        '\u{0C}' => "f".into(),
                        '\r' => "r".into(),
                        '\u{1B}' => "e".into(),
                        '"' => "\"".into(),
                        '\\' => "\\".into(),
                        '\u{85}' => "N".into(),
                        '\u{A0}' => "_".into(),
                        '\u{2028}' => "L".into(),
                        '\u{2029}' => "P".into(),
                        c if (c as u32) <= 0xFF => format!("x{:02X}", c as u32),
                        c if (c as u32) <= 0xFFFF => format!("u{:04X}", c as u32),
                        c => format!("U{:08X}", c as u32),
                    };
                    self.write(&format!("\\{esc}"));
                    start = end + 1;
                }
            }
            // end - start is -1 right after an escape (start = end + 1); Python's int arithmetic, kept
            if 0 < end && end + 1 < t.len() && (ch == Some(' ') || start >= end) && self.column as isize + (end as isize - start as isize) > WIDTH as isize && split {
                let mut d: String = if start < end { t[start..end].iter().collect() } else { String::new() };
                d.push('\\');
                if start < end {
                    start = end;
                }
                self.write(&d);
                self.write_indent();
                self.whitespace = false;
                self.indention = false;
                if t[start] == ' ' {
                    self.write("\\");
                }
            }
            end += 1;
        }
        self.write_indicator("\"", false, false, false);
    }
}

/// safe_dump(v, allow_unicode=True, sort_keys=False, width=100)
pub fn dump(v: &Value) -> String {
    let mut e = Emitter { whitespace: true, indention: true, ..Default::default() };
    // an empty root scalar makes the document explicit ('--- ""' and the like); the table never has one
    e.node(v, true, false, false);
    e.write_indent(); // document end
    if e.open_ended {
        e.write_indicator("...", true, false, false);
        e.write_indent();
    }
    e.out
}

#[cfg(test)]
mod tests {
    use serde_json::json;
    #[test]
    fn basics() {
        assert_eq!(super::dump(&json!([])), "[]\n");
        assert_eq!(super::dump(&json!([{"a": "x", "b": [1, 2], "c": null, "d": [], "e": "yes", "f": 1.5}])),
            "- a: x\n  b:\n  - 1\n  - 2\n  c: null\n  d: []\n  e: 'yes'\n  f: 1.5\n");
        assert_eq!(super::float_repr(1e17), "1.0e+17");
        assert_eq!(super::float_repr(0.0001), "0.0001");
        assert_eq!(super::float_repr(0.00001), "1.0e-05");
        assert_eq!(super::float_repr(2.0), "2.0");
    }
}

// ---------------------------------------------------------------- safe_load (YAML 1.1 typing)
use yaml_rust2::parser::{Event, MarkedEventReceiver, Parser};
use yaml_rust2::scanner::{Marker, TScalarStyle};

/// PyYAML's constructors for a plain scalar: the resolver picks the type, then construct_yaml_*.
/// ponytail: a timestamp stays its text (PyYAML makes a date); the table never holds one, and if a
/// hand edit adds one, the next Rust write quotes it, which still reads back as the same text.
fn construct_plain(v: &str) -> Value {
    let first = v.chars().next();
    let tag = RESOLVERS
        .iter()
        .find(|(chars, _, r)| match first {
            None => chars.contains('n') && r.is_match(""),
            Some(c) => chars.contains(c) && r.is_match(v),
        })
        .map(|x| x.1);
    let signed = |s: &str| -> (i64, String) {
        match s.strip_prefix('-') {
            Some(r) => (-1, r.to_string()),
            None => (1, s.strip_prefix('+').unwrap_or(s).to_string()),
        }
    };
    match tag {
        Some("null") => Value::Null,
        Some("bool") => Value::Bool(matches!(v.to_lowercase().as_str(), "yes" | "true" | "on")),
        Some("int") => {
            let (sign, s) = signed(&v.replace('_', ""));
            let n = if s == "0" {
                Some(0)
            } else if let Some(b) = s.strip_prefix("0b") {
                i64::from_str_radix(b, 2).ok()
            } else if let Some(h) = s.strip_prefix("0x") {
                i64::from_str_radix(h, 16).ok()
            } else if s.starts_with('0') {
                i64::from_str_radix(&s, 8).ok()
            } else if s.contains(':') {
                s.split(':').try_fold(0i64, |acc, d| d.parse::<i64>().ok().map(|d| acc * 60 + d))
            } else {
                s.parse().ok()
            };
            n.map(|n| Value::from(sign * n)).unwrap_or_else(|| Value::String(v.into()))
        }
        Some("float") => {
            let (sign, s) = signed(&v.replace('_', "").to_lowercase());
            let f = if s == ".inf" {
                Some(f64::INFINITY)
            } else if s == ".nan" {
                Some(f64::NAN)
            } else if s.contains(':') {
                s.split(':').try_fold(0f64, |acc, d| d.parse::<f64>().ok().map(|d| acc * 60.0 + d))
            } else {
                s.parse().ok()
            };
            f.and_then(|f| serde_json::Number::from_f64(sign as f64 * f)).map(Value::Number).unwrap_or(Value::Null)
        }
        _ => Value::String(v.into()),
    }
}

/// The quoting of every scalar, in document order (keys included), from yaml-rust2's events.
#[derive(Default)]
struct Styles {
    plain: Vec<(bool, String)>,
    alias: bool,
}

impl MarkedEventReceiver for Styles {
    fn on_event(&mut self, ev: Event, _: Marker) {
        match ev {
            Event::Scalar(text, style, _, _) => self.plain.push((style == TScalarStyle::Plain, text)),
            Event::Alias(_) => self.alias = true,
            _ => {}
        }
    }
}

/// Retype the unquoted scalars of `v` by PyYAML's resolver, walking it in document order.
fn retype(v: &mut Value, styles: &[(bool, String)], i: &mut usize) -> bool {
    match v {
        Value::Object(m) => m.values_mut().all(|x| {
            *i += 1; // the key: keys stay strings
            retype(x, styles, i)
        }),
        Value::Array(a) => a.iter_mut().all(|x| retype(x, styles, i)),
        _ => {
            let Some((plain, text)) = styles.get(*i) else { return false };
            *i += 1;
            if *plain {
                let typed = construct_plain(text);
                // a plain string keeps libyaml's reading of it; only a typed token takes the 1.1 type
                if !typed.is_string() {
                    *v = typed;
                } else if !v.is_string() {
                    *v = Value::String(text.clone());
                }
            } else if !v.is_string() {
                *v = Value::String(text.clone());
            }
            true
        }
    }
}

/// safe_load: the first document's value, typed as PyYAML types it (null for an empty stream).
/// serde_yaml_ng (a libyaml port, as PyYAML follows libyaml) reads the text, so quoted strings and
/// their line folding match exactly; yaml-rust2's events say which scalars were plain, and those
/// are retyped by YAML 1.1 (`yes`, `1:30` and `017` are not strings there; `1e3` and `0o7` are).
pub fn load(text: &str) -> Result<Value, String> {
    let mut v: Value = serde_yaml_ng::from_str(text).map_err(|e| e.to_string())?;
    let mut st = Styles::default();
    // yaml-rust2 refuses a few strings mixing NEL or U+2028 with blank lines that libyaml reads; there
    // libyaml's (YAML 1.2) typing stands, wrong only for an unquoted `1e3` or `0o7` in the same file
    if Parser::new_from_str(text).load(&mut st, false).is_err() {
        return Ok(v);
    }
    let mut i = 0;
    let mut typed = v.clone();
    // ponytail: an alias or a repeated key breaks the one-to-one walk; libyaml's typing then stands
    if !st.alias && retype(&mut typed, &st.plain, &mut i) && i == st.plain.len() {
        v = typed;
    }
    Ok(v)
}

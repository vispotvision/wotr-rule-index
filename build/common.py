"""Shared loading and normalisation for the WOTR rule index."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
SOURCES_DIR = ROOT / "sources"
OUT_DIR = ROOT / "out"
SCHEMA = ROOT / "schema" / "rule.schema.json"
VOCAB_DOC = ROOT / "schema" / "applies_to.md"

try:
    import yaml
except ImportError:
    sys.exit("pyyaml missing. run: pip install pyyaml jsonschema")


def normalise(text: str) -> str:
    """Strip markdown emphasis and collapse whitespace, so a verbatim quote can
    match the source without carrying its asterisks and line breaks."""
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_vocab() -> set:
    """applies_to tags are the backticked cells in the vocabulary table."""
    body = VOCAB_DOC.read_text(encoding="utf-8")
    return set(re.findall(r"^\|\s*`([a-z-]+)`", body, flags=re.M))


def load_rule_files():
    for path in sorted(RULES_DIR.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not doc or "rules" not in doc:
            continue
        yield path, doc


def load_rules():
    """Flat list of every rule row, each carrying _file for error reporting."""
    rows = []
    for path, doc in load_rule_files():
        for rule in doc.get("rules") or []:
            rule = dict(rule)
            rule["_file"] = path.name
            rows.append(rule)
    return rows


def load_schema():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))

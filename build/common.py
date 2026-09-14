"""Shared loading and normalisation for the WOTR rule index."""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
SOURCES_DIR = ROOT / "sources"
OUT_DIR = ROOT / "out"
SCHEMA = ROOT / "schema" / "rule.schema.json"
VOCAB_DOC = ROOT / "schema" / "applies_to.md"


# --------------------------------------------------------------------------
# machine configuration: ~/.config/wotr/env (see build/wotr.env.example)
#
# On Windows every tool read NOTION_TOKEN and friends out of the registry when
# they were not in the environment. On Linux the equivalent is one file that the
# shell scripts source (build/env.sh), the systemd units load (EnvironmentFile=)
# and this loader reads — so a process started by Claude Desktop, which inherits
# no shell profile, still finds the same values. Nothing here overrides a
# variable that is already set.

ENV_FILE = Path(os.environ.get("WOTR_ENV_FILE") or Path.home() / ".config" / "wotr" / "env")


def load_env(path: Path = ENV_FILE) -> dict:
    """Read KEY=value lines into os.environ where the key is unset or empty.
    Reads the file the way systemd and build/env.sh do: one pair of quotes and
    the surrounding whitespace stripped, a line without '=' ignored; a leading ~
    is expanded as env.sh expands it. Returns what was loaded. Quiet when the
    file is missing."""
    loaded = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return loaded
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\'\"":
            val = val[1:-1]
        if val == "~" or val.startswith("~/"):
            val = os.path.expanduser(val)
        if key and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) and val and not os.environ.get(key):
            os.environ[key] = val
            loaded[key] = val
    return loaded


load_env()


def env_path(key: str, default: str | None) -> Path | None:
    """A path from the environment (~ expanded), or the default, or None."""
    raw = os.environ.get(key) or default
    return Path(raw).expanduser() if raw else None


# the base craft guides and their dated editions — in no git repository
TRUE_CANON = env_path("WOTR_TRUE_CANON", "~/wotr-vault/true-canon")
# the TTS engines' interpreters live at <VENVS>/wotr-<engine>/bin/python
VENVS = env_path("WOTR_VENVS", "~/.venvs")
# Google Drive when it is mounted (rclone); None means "skip the Drive exports"
DRIVE = env_path("WOTR_DRIVE", None)
# the weekly zip lands here when Drive is not mounted
BACKUP_DIR = env_path("WOTR_BACKUP_DIR", "~/wotr-backups")


def drive_dir(*parts: str) -> Path | None:
    """<WOTR_DRIVE>/<parts> if Drive is configured and mounted, else None."""
    if DRIVE and DRIVE.is_dir():
        return DRIVE.joinpath(*parts)
    return None


def venv_python(name: str) -> Path:
    """The interpreter of the TTS venv <VENVS>/wotr-<name> (Linux layout)."""
    return VENVS / f"wotr-{name}" / "bin" / "python"

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

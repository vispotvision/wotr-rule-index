#!/usr/bin/env python3
"""Weekly backup of the canon to Google Drive: one zip of wiki/, scenes/, table/, rules/,
sources/, proposals/, reports/ and the top-level ledgers into
  G:\\My Drive\\War of the Realms — Backups\\wotr-<date>.zip
keeping the last twelve. A file another process holds open is skipped and named in the log.
Run by build/backup.ps1 (the scheduled task "WOTR weekly backup", Sunday 03:00)."""
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = Path(r"G:\My Drive\War of the Realms — Backups")
ITEMS = ["wiki", "scenes", "table", "rules", "sources", "proposals", "reports", "docs", "RULINGS.md", "CONFLICTS.md", "ROADMAP.md", "CONTINUE.md", "README.md"]
KEEP = 12
LOG = ROOT / "build" / "backup.log"


def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    if not DEST.parent.exists():
        log("G:\\My Drive not mounted; skipped")
        return 0
    DEST.mkdir(parents=True, exist_ok=True)
    out = DEST / f"wotr-{datetime.now():%Y-%m-%d}.zip"
    skipped, n = [], 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in ITEMS:
            p = ROOT / item
            if not p.exists():
                continue
            files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
            for f in files:
                try:
                    z.write(f, f.relative_to(ROOT).as_posix())
                    n += 1
                except OSError as e:
                    skipped.append(f"{f.relative_to(ROOT).as_posix()} ({e.strerror})")
    log(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {n} files)" + (f"; skipped {len(skipped)}: " + "; ".join(skipped[:5]) if skipped else ""))
    old = sorted(DEST.glob("wotr-*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)[KEEP:]
    for f in old:
        f.unlink()
        log(f"pruned {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

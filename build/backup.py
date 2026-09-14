#!/usr/bin/env python3
"""Weekly backup of the canon: one zip of wiki/, scenes/, table/, rules/, sources/,
proposals/, reports/, the top-level ledgers and the WOTR True Canon folder (the base
guides and their dated editions, which live in no git repository) into
  <WOTR_DRIVE>/War of the Realms — Backups/wotr-<date>.zip   when Drive is mounted,
  <WOTR_BACKUP_DIR>/wotr-<date>.zip                           otherwise (~/wotr-backups),
keeping the last twelve. A file another process holds open is skipped and named in the log.
Both paths come from ~/.config/wotr/env (build/wotr.env.example).
Run by build/backup.sh (the systemd user timer wotr-backup.timer, Sunday 03:00)."""
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402

ROOT = common.ROOT
# Drive when it is mounted (was G:\My Drive\War of the Realms — Backups); the local
# backup directory otherwise — on Linux the backup always happens, Drive or not
DRIVE_DEST = common.drive_dir("War of the Realms — Backups")
DEST = DRIVE_DEST or common.BACKUP_DIR
ITEMS = ["wiki", "scenes", "table", "rules", "sources", "proposals", "reports", "docs", "RULINGS.md", "CONFLICTS.md", "ROADMAP.md", "CONTINUE.md", "README.md"]
# outside the repo and in no git history: the base craft guides and their dated
# editions (WOTR_TRUE_CANON; was Documents\WOTR True Canon). A Drive mirror of that
# folder carries a rollback with it (it has, once); these zips are the versions.
EXTRA = [common.TRUE_CANON]
KEEP = 12
LOG = ROOT / "build" / "backup.log"


def log(msg: str) -> None:
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def main() -> int:
    if DRIVE_DEST is None:
        log(f"Drive not mounted; writing to {DEST}")
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
        for folder in EXTRA:
            if not folder.exists():
                log(f"{folder} not found; skipped")
                continue
            for f in folder.rglob("*"):
                if not f.is_file():
                    continue
                try:
                    z.write(f, f"{folder.name}/{f.relative_to(folder).as_posix()}")
                    n += 1
                except OSError as e:
                    skipped.append(f"{folder.name}/{f.relative_to(folder).as_posix()} ({e.strerror})")
    log(f"wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {n} files)" + (f"; skipped {len(skipped)}: " + "; ".join(skipped[:5]) if skipped else ""))
    old = sorted(DEST.glob("wotr-*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)[KEEP:]
    for f in old:
        f.unlink()
        log(f"pruned {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

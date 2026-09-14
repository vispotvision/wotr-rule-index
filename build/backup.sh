#!/usr/bin/env bash
# Weekly backup of the canon (see build/backup.py): one zip to Google Drive when it is
# mounted (WOTR_DRIVE), to WOTR_BACKUP_DIR (~/wotr-backups) otherwise; the last twelve
# kept. Runs as the systemd user timer wotr-backup.timer (Sunday 03:00; the unit files
# are in build/systemd/, build/systemd_setup.sh installs them).
#
#   bash build/backup.sh
#
# Remove with: systemctl --user disable --now wotr-backup.timer
#
# (was build/backup.ps1 and the scheduled task "WOTR weekly backup")

set -uo pipefail
. "$(dirname "$0")/env.sh"

# exec: the interpreter takes over the process, so its exit code is the script's
exec "$WOTR_PYTHON" build/backup.py

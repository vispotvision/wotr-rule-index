#!/usr/bin/env bash
# Run a WOTR tool in the project's interpreter, from the repo, with the env loaded.
#
#   bash build/py.sh build/jobs_server.py --port 8799 --log build/.jobs_server.log
#   bash build/py.sh build/validate.py
#
# The long-running systemd units (wotr-jobs, wotr-mcp-public) go through this because
# ExecStart= cannot take a variable as the executable (was: the logon tasks named the
# Store Python's exe by its full path). env.sh cds to the repo, loads ~/.config/wotr/env
# and picks $WOTR_PYTHON; then this execs it, so the tool is the unit's main process —
# signals reach it and the exit code is its own. Nothing to remove: it registers nothing.

set -uo pipefail
. "$(dirname "$0")/env.sh"
exec "$WOTR_PYTHON" "$@"

# shellcheck shell=bash
# The shared prelude for every WOTR shell script. Source it; never run it.
#
#   . "$(dirname "$0")/env.sh"          # from build/*.sh
#   . "$(dirname "$0")/../build/env.sh" # from bot/run.sh
#
# What it does, in order:
#   1. finds the repo from its own location and cd's there
#   2. loads ~/.config/wotr/env (secrets and machine paths; see build/wotr.env.example)
#      without overriding anything already in the environment — a terminal's exports win
#      over the file. Under a unit, systemd has read the same file first (EnvironmentFile=,
#      which beats the unit's own Environment=), so the file is the place to override a
#      value, never Environment=. The file is read the way systemd and common.load_env()
#      read it — one pair of quotes and the surrounding whitespace stripped, a CR ignored,
#      a line without '=' ignored — so a value means the same thing in a terminal, in a
#      unit and in a Python tool.
#   3. picks the interpreter: $WOTR_PYTHON, else ~/.venvs/wotr/bin/python, else python3
#   4. finds the Claude Code CLI: $WOTR_CLAUDE, else `claude` on PATH, else mise's shim
#   5. defines wotr_log "message": timestamped, to $WOTR_LOG (if set) and stdout
#
# This replaces what the PowerShell scripts each did by hand on Windows (the registry
# lookup for NOTION_TOKEN, the hard-coded Store Python, $env:USERPROFILE\.local\bin\claude.exe).

: "${HOME:?HOME is not set; env.sh needs it for ~/.config/wotr/env and the venv}"

WOTR_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
export WOTR_REPO
cd "$WOTR_REPO" || exit 1

WOTR_ENV_FILE="${WOTR_ENV_FILE:-$HOME/.config/wotr/env}"
if [ -f "$WOTR_ENV_FILE" ]; then
    # every KEY=value line becomes an export, but only where the variable is unset
    # or empty in the current environment
    while IFS= read -r _line || [ -n "$_line" ]; do
        _line="${_line%$'\r'}"                                  # a CRLF file still parses
        case "$_line" in ''|'#'*|';'*) continue ;; esac
        case "$_line" in *=*) ;; *) continue ;; esac            # no '=': not an assignment
        _key="${_line%%=*}"; _val="${_line#*=}"
        case "$_key" in ''|[0-9]*|*[!A-Za-z0-9_]*) continue ;; esac
        _val="${_val#"${_val%%[![:space:]]*}"}"                 # surrounding whitespace
        _val="${_val%"${_val##*[![:space:]]}"}"
        case "$_val" in \"*\"|\'*\')                             # one matching pair of quotes
            [ ${#_val} -ge 2 ] && _val="${_val:1:${#_val}-2}" ;;
        esac
        _cur="${!_key:-}"
        [ -n "$_cur" ] || _cur="$_val"
        # a leading ~ is expanded whichever side supplied the value: systemd hands the
        # file's ~ over untouched and common.env_path() expands it, so this is what keeps
        # a unit, a terminal and the Python tools on the same path
        case "$_cur" in '~') _cur="$HOME" ;; '~/'*) _cur="$HOME/${_cur#'~/'}" ;; esac
        if [ -n "$_cur" ]; then export "$_key=$_cur"; fi
    done < "$WOTR_ENV_FILE"
    unset _line _key _val _cur
fi

# the interpreter. A WOTR_PYTHON that is not there is said so on stderr (the journal,
# under a unit) rather than swapped quietly for a system python that lacks the packages;
# the fallback then goes venv first, PATH last.
if [ -n "${WOTR_PYTHON:-}" ] && [ ! -x "$WOTR_PYTHON" ]; then
    printf 'env.sh: WOTR_PYTHON=%s is not an executable; ignoring it\n' "$WOTR_PYTHON" >&2
    WOTR_PYTHON=""
fi
if [ -z "${WOTR_PYTHON:-}" ]; then
    WOTR_PYTHON="$HOME/.venvs/wotr/bin/python"
    if [ ! -x "$WOTR_PYTHON" ]; then
        printf 'env.sh: no interpreter at %s; using the python3 on PATH (build/setup_linux.sh makes the venv)\n' "$WOTR_PYTHON" >&2
        WOTR_PYTHON="$(command -v python3 || command -v python || true)"
    fi
fi
export WOTR_PYTHON
# the venv's bin/ goes first on PATH, so a bare `python` in anything a script starts
# (the headless Claude's "python build/book_tools.py", a worker, a hook) is the same
# interpreter — the Windows sync once ran a package-less 3.10 that way and failed silently.
# Sourced twice (a script that sources another), it is prepended once.
case "$WOTR_PYTHON" in */bin/python|*/bin/python3)
    _bin="$(dirname "$WOTR_PYTHON")"
    case "$PATH" in "$_bin":*|"$_bin") ;; *) PATH="$_bin:$PATH"; export PATH ;; esac
    unset _bin ;;
esac

if [ -z "${WOTR_CLAUDE:-}" ] || [ ! -x "${WOTR_CLAUDE:-}" ]; then
    WOTR_CLAUDE="$(command -v claude 2>/dev/null || true)"
    [ -n "$WOTR_CLAUDE" ] || WOTR_CLAUDE="$HOME/.local/share/mise/shims/claude"
fi
export WOTR_CLAUDE

export PYTHONIOENCODING=utf-8 PYTHONUNBUFFERED=1 LANG="${LANG:-C.UTF-8}"

# wotr_log "text": one timestamped line to $WOTR_LOG (appended) and to stdout
wotr_log() {
    local line
    line="$(date '+%Y-%m-%d %H:%M:%S')  $*"
    if [ -n "${WOTR_LOG:-}" ]; then printf '%s\n' "$line" >> "$WOTR_LOG"; fi
    printf '%s\n' "$line"
}

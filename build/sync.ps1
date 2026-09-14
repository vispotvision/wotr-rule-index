# Two-way mirror: Notion wiki -> wiki/, then repo scenes and index outputs
# -> Notion, then commit and push whatever changed.
#
#   powershell -ExecutionPolicy Bypass -File build\sync.ps1
#
# This is what turns "Natalie archived a scene in Notion" into "the scene is
# in the repo": her session-end protocol files the scene under the wiki's
# Scene Archive section; this script mirrors it to wiki/The Scene Archive/
# and commits it. Safe to run any time; if nothing changed, nothing is
# committed. Needs NOTION_TOKEN as a user environment variable and git
# credentials already set up (gh auth login did that).
#
# To run it on a schedule (hourly, while logged in), register once from an
# elevated-or-not PowerShell:
#
#   $a = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\build\sync.ps1`"" -WorkingDirectory "$PWD"
#   $t = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
#   Register-ScheduledTask -TaskName "WOTR wiki sync" -Action $a -Trigger $t -Description "Mirror the Notion wiki into the wotr-rule-index repo and push"
#
# Remove with: Unregister-ScheduledTask -TaskName "WOTR wiki sync" -Confirm:$false

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$log = Join-Path $repo "build\sync.log"
function Log($msg) { $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg; $line | Out-File -Append -Encoding utf8 $log; Write-Host $line }

if (-not $env:NOTION_TOKEN) { $env:NOTION_TOKEN = [Environment]::GetEnvironmentVariable("NOTION_TOKEN", "User") }
if (-not $env:NOTION_TOKEN) { Log "NOTION_TOKEN not set; aborting"; exit 1 }

# One interpreter for every step: the 3.13 the MCP and the tools were installed into
# (build/install_mcp.ps1 registers the same path). A bare `python` resolves to a different,
# package-less 3.10 when this script is launched from Claude Desktop or the scheduled task.
$python = $env:WOTR_PYTHON
if (-not $python) { $python = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe" }
if (-not (Test-Path $python)) { $python = (Get-Command python).Source }
Log "python: $python"

Log "export start"
$out = & $python build\notion_export.py 2>&1
$code = $LASTEXITCODE
$out | Select-Object -Last 3 | ForEach-Object { Log "  $_" }
if ($code -ne 0) { Log "export failed (exit $code)"; exit $code }

# semantic index over wiki/ and scenes/ for the MCP's wiki and scene_recall
# (build/index/, gitignored; only chunks whose text changed get re-embedded)
Log "embed start"
# The index is a convenience; a failure here must never stop the publish, commit and push
# below (under ErrorActionPreference=Stop a stderr line from python is a terminating error).
try {
    $out = & $python build\embed_index.py 2>&1 | ForEach-Object { "$_" }
    if ($LASTEXITCODE -ne 0) {
        Log "embed failed (exit $LASTEXITCODE) with python at $((Get-Command python).Source)"
        $out | Select-Object -Last 6 | ForEach-Object { Log "    $_" }
    } else {
        $out | Select-Object -Last 1 | ForEach-Object { Log "  $_" }
    }
} catch {
    Log "embed failed: $($_.Exception.Message) (python at $python)"
}

# the Obsidian view (vault/, gitignored): the mirror with [[wikilinks]] injected
try { & $python build\vault_export.py 2>&1 | Select-Object -Last 1 | ForEach-Object { Log "  $_" } } catch { Log "vault failed: $($_.Exception.Message)" }

# the other direction: index outputs and scenes that changed in the repo go
# up to Notion (build/notion_publish.py is idempotent; unchanged files are skipped)
Log "publish start"
$out = & $python build\notion_publish.py 2>&1
$out | Select-Object -Last 2 | ForEach-Object { Log "  $_" }
if ($LASTEXITCODE -ne 0) { Log "publish failed (exit $LASTEXITCODE)" }

# Word documents for the Google Drive folder (Drive for Desktop syncs G:\My Drive)
$docs = "G:\My Drive\War of the Realms — Documents"
if (Test-Path "G:\My Drive") {
    Log "docs start"
    $out = & $python build\docs_export.py --out $docs --private-out "G:\My Drive\War of the Realms — Private" 2>&1
    $out | Select-Object -Last 1 | ForEach-Object { Log "  $_" }
    $out = & $python build\arcs_export.py --out "$docs\Arcs" 2>&1
    $out | Select-Object -Last 1 | ForEach-Object { Log "  $_" }
} else { Log "G:\My Drive not mounted; docs skipped" }

# make sure we are not committing on top of a stale checkout. Git writes warnings to stderr
# (CRLF notices, worktree prune failures) and under ErrorActionPreference=Stop a stderr line
# is a terminating error, which killed every run of 2026-09-13 before its push; so git runs
# with errors demoted, and only exit codes are judged.
$ErrorActionPreference = "Continue"
& git pull -q --rebase origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "pull --rebase failed (exit $LASTEXITCODE); committing on the local branch anyway" }

$changes = & git status --porcelain -- wiki table scenes/CAST.md scenes/TIMELINE.md build/.notion_publish.json
if (-not $changes) { Log "no wiki changes"; exit 0 }

$n = ($changes | Measure-Object).Count
& git add -- wiki table scenes/CAST.md scenes/TIMELINE.md build/.notion_publish.json
& git commit -q -m "Wiki sync: $n file(s) changed in Notion`n`nAutomated mirror of the War of the Realms wiki via build/sync.ps1." 2>&1 | Out-Null
& git push -q origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "push failed"; exit 1 }
Log "pushed $n file(s)"

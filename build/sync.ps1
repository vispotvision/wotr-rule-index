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

Log "export start"
$out = & python build\notion_export.py 2>&1
$code = $LASTEXITCODE
$out | Select-Object -Last 3 | ForEach-Object { Log "  $_" }
if ($code -ne 0) { Log "export failed (exit $code)"; exit $code }

# the other direction: index outputs and scenes that changed in the repo go
# up to Notion (build/notion_publish.py is idempotent; unchanged files are skipped)
Log "publish start"
$out = & python build\notion_publish.py 2>&1
$out | Select-Object -Last 2 | ForEach-Object { Log "  $_" }
if ($LASTEXITCODE -ne 0) { Log "publish failed (exit $LASTEXITCODE)" }

# make sure we are not committing on top of a stale checkout
& git pull -q --rebase origin master 2>&1 | Out-Null

$changes = & git status --porcelain -- wiki build/.notion_publish.json
if (-not $changes) { Log "no wiki changes"; exit 0 }

$n = ($changes | Measure-Object).Count
& git add -- wiki build/.notion_publish.json
& git commit -q -m "Wiki sync: $n file(s) changed in Notion`n`nAutomated mirror of the War of the Realms wiki via build/sync.ps1." 2>&1 | Out-Null
& git push -q origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "push failed"; exit 1 }
Log "pushed $n file(s)"

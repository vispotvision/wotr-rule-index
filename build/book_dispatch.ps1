# The book dispatcher: one chapter a night, while Isaac sleeps.
#
# build/book_next.py says what the book needs (write the next chapter, or stop because a
# gate chapter is written and undecided). If a chapter is due, Claude Code runs headless
# on the subscription (build/book_dispatch_prompt.md) and invokes the book-chapter
# workflow, which does the real work: brief -> draft -> ten check passes -> bounded
# revise -> gate digest, all under book/<slug>/ch<NN>/. Then this script commits what
# landed. Isaac approves or rejects at breakfast; the nightly digest (03:30) shows him
# where the book stands.
#
# Registered as the scheduled task "WOTR book" (daily 02:00):
#   $a = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\build\book_dispatch.ps1`"" -WorkingDirectory "$PWD"
#   $t = New-ScheduledTaskTrigger -Daily -At 2:00am
#   Register-ScheduledTask -TaskName "WOTR book" -Action $a -Trigger $t -Settings (New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 5))
# Remove with: Unregister-ScheduledTask -TaskName "WOTR book" -Confirm:$false
#
# Off switch: set WOTR_BOOK_OFF=1 (user env var). One chapter per run, always.
#   -Slug <name>   another book under book/
#   -DryRun        decide and report; never call Claude

param([string]$Slug = "kharven-year", [switch]$DryRun)

$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$log = Join-Path $repo "build\book_dispatch.log"
function Log($msg) { $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg; $line | Out-File -Append -Encoding utf8 $log; Write-Host $line }

$python = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
if (-not (Test-Path $python)) { $python = (Get-Command python).Source }
$env:PYTHONIOENCODING = "utf-8"

$off = $env:WOTR_BOOK_OFF; if (-not $off) { $off = [Environment]::GetEnvironmentVariable("WOTR_BOOK_OFF", "User") }
if ($off) { Log "WOTR_BOOK_OFF is set; nothing dispatched"; exit 0 }

Log "dispatch start ($Slug)"
& git pull -q --rebase --autostash origin master 2>&1 | Out-Null  # a tracked log churns; autostash keeps the rebase from refusing
if ($LASTEXITCODE -ne 0) { Log "pull --rebase failed (exit $LASTEXITCODE); running on the local branch" }

$raw = & $python build\book_next.py --slug $Slug --json 2>&1
try { $next = $raw | ConvertFrom-Json } catch { Log "book_next.py said: $raw"; exit 1 }
Log "  next: $($next.action) — $($next.why)"
if ($next.action -ne "write" -and $next.action -ne "rewrite") { Log "nothing to write tonight"; exit 0 }
if ($DryRun) { Log "dry run: would write chapter $($next.chapter)"; exit 0 }

$claude = "$env:USERPROFILE\.local\bin\claude.exe"
if (-not (Test-Path $claude)) { Log "claude CLI not found at $claude"; exit 1 }

Log "  chapter $($next.chapter): claude start (this takes an hour or more)"
$t0 = Get-Date
# called directly, not through Start-Job: the job subsystem hung after the child had
# exited (2026-09-13). The task's ExecutionTimeLimit (5 h) is the timeout; if Windows
# kills the run mid-chapter, the next night's run commits whatever landed and goes on.
# The prompt goes in on stdin: passed as an argument, PowerShell strips the quotes out
# of it before claude.exe ever sees them, and the script inside it stops parsing.
$res = Get-Content -Raw -Encoding utf8 "build\book_dispatch_prompt.md" | & $claude -p --max-turns 120 --permission-mode acceptEdits `
    --allowedTools "Workflow" "Read" "Write" "Edit" "Glob" "Grep" "TaskOutput" "Bash(python build/book_tools.py:*)" "Bash(python build/book_next.py:*)" 2>&1
$tail = ($res | Select-Object -Last 3) -join " "
Log ("  claude done in {0} min: {1}" -f [int]((Get-Date) - $t0).TotalMinutes, $tail.Substring(0, [Math]::Min(400, $tail.Length)))

# refresh GATES.md from whatever is on disk now, then commit the chapter
& $python build\book_next.py --slug $Slug 2>&1 | ForEach-Object { Log "  $_" }
$changes = & git status --porcelain -- book
if (-not $changes) { Log "nothing new under book/; done"; exit 0 }
$n = ($changes | Measure-Object).Count
& git add -- book
& git commit -q -m "Book $($Slug): chapter $($next.chapter) drafted overnight`n`nAutomated: build/book_dispatch.ps1. Nothing archived; the gate is Isaac's." 2>&1 | Out-Null
& git push -q origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "push failed (the sync will carry it up)" }
Log "committed $n file(s) under book/"

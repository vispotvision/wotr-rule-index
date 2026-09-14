# The nightly checks: build/nightly.py (validate, resolve, the audits, the Büri sweep,
# the diff against last night -> reports/nightly.md), then Claude Code on the
# subscription writes the "Overnight" note at the top (build/nightly_prompt.md; the
# only file it may edit is reports/nightly.md), then the digest and the audit
# reports are committed and pushed. session_start shows the note next morning.
#
# Registered as the scheduled task "WOTR nightly" (daily 03:30):
#   $a = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$PWD\build\nightly.ps1`"" -WorkingDirectory "$PWD"
#   $t = New-ScheduledTaskTrigger -Daily -At 3:30am
#   Register-ScheduledTask -TaskName "WOTR nightly" -Action $a -Trigger $t -Settings (New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2))
# Remove with: Unregister-ScheduledTask -TaskName "WOTR nightly" -Confirm:$false
#
# Set WOTR_NIGHTLY_NO_CLAUDE=1 (user env var) to run the numbers only.

$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$log = Join-Path $repo "build\nightly.log"
function Log($msg) { $line = "{0}  {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg; $line | Out-File -Append -Encoding utf8 $log; Write-Host $line }

$python = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
if (-not (Test-Path $python)) { $python = (Get-Command python).Source }
$env:PYTHONIOENCODING = "utf-8"
if (-not $env:NOTION_TOKEN) { $env:NOTION_TOKEN = [Environment]::GetEnvironmentVariable("NOTION_TOKEN", "User") }

Log "nightly start"
& git pull -q --rebase origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "pull --rebase failed (exit $LASTEXITCODE); running on the local branch" }

$out = & $python build\nightly.py 2>&1
$code = $LASTEXITCODE
$out | Select-Object -Last 2 | ForEach-Object { Log "  $_" }
if (-not (Test-Path "reports\nightly.md")) { Log "no digest written (exit $code); stopping"; exit 1 }

# the Overnight note: Claude Code, headless, on the subscription; tools locked to reading,
# the read-only CLI, and editing the digest itself
$claude = "$env:USERPROFILE\.local\bin\claude.exe"
$noClaude = $env:WOTR_NIGHTLY_NO_CLAUDE
if (-not $noClaude) { $noClaude = [Environment]::GetEnvironmentVariable("WOTR_NIGHTLY_NO_CLAUDE", "User") }
if ((Test-Path $claude) -and -not $noClaude) {
    Log "claude start"
    $prompt = Get-Content -Raw -Encoding utf8 "build\nightly_prompt.md"
    $job = Start-Job -ScriptBlock {
        param($claude, $prompt, $repo)
        Set-Location $repo
        $env:PYTHONIOENCODING = "utf-8"
        & $claude -p $prompt --max-turns 40 --allowedTools "Read" "Edit(reports/nightly.md)" "Bash(python build/book_tools.py:*)" 2>&1
    } -ArgumentList $claude, $prompt, $repo
    if (Wait-Job $job -Timeout 1500) {
        $res = Receive-Job $job
        Log ("  claude: " + (($res | Select-Object -Last 1) -join " ").Substring(0, [Math]::Min(160, (($res | Select-Object -Last 1) -join " ").Length)))
    } else {
        Stop-Job $job; Log "  claude: timed out after 25 min; the digest stands without the note"
    }
    Remove-Job $job -Force
    if (Select-String -Path "reports\nightly.md" -Pattern "Claude's note goes here" -Quiet) { Log "  claude: note not written" } else { Log "  claude: note written" }
} else { Log "claude step skipped" }

# commit the digest and the audit reports; nothing else
$paths = @("reports/nightly.md", "reports/prose_pass.md", "reports/recurrence.md", "reports/reconcile.md", "build/.nightly_state.json", "out")
$changes = & git status --porcelain -- $paths
if (-not $changes) { Log "nothing to commit"; exit 0 }
& git add -- $paths
& git commit -q -m "Nightly $(Get-Date -Format 'yyyy-MM-dd'): the checks and the overnight note`n`nAutomated: build/nightly.ps1." 2>&1 | Out-Null
& git push -q origin master 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Log "push failed (the sync will carry it up)"; exit 0 }
Log "committed and pushed"

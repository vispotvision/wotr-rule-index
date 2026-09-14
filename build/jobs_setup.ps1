# Register the job runner as the logon task "WOTR jobs" (build/jobs_server.py on
# 127.0.0.1:8799), so n8n can start WOTR work on this machine whenever it likes.
#   powershell -ExecutionPolicy Bypass -File build\jobs_setup.ps1
#   powershell -ExecutionPolicy Bypass -File build\jobs_setup.ps1 -Remove
#
# The listener is loopback-only. Docker Desktop lets a container reach the host's
# loopback as host.docker.internal, so n8n gets in and nothing on the LAN does.
# The shared secret lives in build/.jobs_token (gitignored) - paste it into n8n once,
# as a header credential; never into a chat, a workflow export or a commit.

param([switch]$Remove)

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$task = "WOTR jobs"

if ($Remove) {
    Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "removed the scheduled task '$task'"
    exit 0
}

$pythonw = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\pythonw.exe"
if (-not (Test-Path $pythonw)) {
    $py = (Get-Command python).Source
    $pythonw = Join-Path (Split-Path -Parent $py) "pythonw.exe"
    if (-not (Test-Path $pythonw)) { $pythonw = $py }   # a console window, but it runs
}

$action = New-ScheduledTaskAction -Execute $pythonw `
    -Argument "build\jobs_server.py --port 8799 --log build\.jobs_server.log" -WorkingDirectory $repo
# -User: an AtLogOn trigger with no user means every user, which needs an elevated shell
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit ([TimeSpan]::Zero)
Register-ScheduledTask -TaskName $task -Action $action -Trigger $trigger -Settings $settings `
    -Description "WOTR job runner for n8n: named jobs only, loopback, shared secret" -Force | Out-Null
Start-ScheduledTask -TaskName $task
Start-Sleep -Seconds 3

try {
    $h = Invoke-RestMethod "http://127.0.0.1:8799/health" -TimeoutSec 5
    Write-Host "'$task' registered and answering. Jobs: $($h.jobs.PSObject.Properties.Name -join ', ')"
} catch {
    Write-Host "'$task' registered, but 127.0.0.1:8799 did not answer yet - check build\.jobs_server.log"
}
Write-Host "The shared secret is in build\.jobs_token. In n8n: Credentials -> Header Auth,"
Write-Host "name X-Job-Token, value that string; then point HTTP Request nodes at"
Write-Host "http://host.docker.internal:8799/ ."

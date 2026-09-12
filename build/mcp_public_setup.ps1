# Share the WOTR MCP with friends: the read-only server behind a shared secret,
# published through Tailscale Funnel.
#
#   powershell -ExecutionPolicy Bypass -File build\mcp_public_setup.ps1
#
# What it does, idempotently:
#   1. writes build\.mcp_token (the shared secret) if it does not exist
#   2. registers the scheduled task "WOTR MCP public" (runs at logon, restarts
#      itself, hidden): pythonw build\mcp_server.py --public --log build\mcp_public.log
#      and starts it now
#   3. tailscale funnel --bg 8765: publishes https://<machine>.<tailnet>.ts.net/
#      -> 127.0.0.1:8765 (Tailscale keeps this across reboots)
#   4. prints the URL to hand out
#
# Needs: Tailscale installed and logged in (tailscale status), and Funnel enabled
# for the tailnet (the first `tailscale funnel` prints a one-click link if not).
#
# The server exposes only the tools that read the repo (READ_ONLY_TOOLS in
# build\mcp_server.py). Nothing a friend does through it can write to the repo,
# the table, Notion, or git. Rotate the secret by deleting build\.mcp_token and
# re-running this script; friends then need the new URL.
#
# Remove with:
#   tailscale funnel --bg off ; Unregister-ScheduledTask -TaskName "WOTR MCP public" -Confirm:$false

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo

$port = 8765
$tokenFile = Join-Path $repo "build\.mcp_token"
$log = Join-Path $repo "build\mcp_public.log"
$pythonw = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\pythonw.exe"
if (-not (Test-Path $pythonw)) { $pythonw = (Get-Command pythonw -ErrorAction Stop).Source }
$tailscale = "C:\Program Files\Tailscale\tailscale.exe"
if (-not (Test-Path $tailscale)) { $tailscale = (Get-Command tailscale -ErrorAction Stop).Source }

# 1. the shared secret
if (-not (Test-Path $tokenFile)) {
    $bytes = New-Object byte[] 24
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $tok = [Convert]::ToBase64String($bytes).TrimEnd('=').Replace('+', '-').Replace('/', '_')
    [IO.File]::WriteAllText($tokenFile, $tok)
    Write-Host "wrote a new shared secret to build\.mcp_token"
}
$token = (Get-Content $tokenFile -Raw).Trim()

# 2. the server as a logon task
$taskName = "WOTR MCP public"
$action = New-ScheduledTaskAction -Execute $pythonw `
    -Argument "`"$repo\build\mcp_server.py`" --public --port $port --log `"$log`"" `
    -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartCount 5 -RestartInterval (New-TimeSpan -Minutes 1) `
    -MultipleInstances IgnoreNew -StartWhenAvailable -Hidden
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings `
    -Description "WOTR MCP, read-only, shared secret required; published by Tailscale Funnel" -Force | Out-Null
$running = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if (-not $running) {
    Start-ScheduledTask -TaskName $taskName
    $deadline = (Get-Date).AddSeconds(20)
    while (-not (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) -and (Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 500
    }
}
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
    Write-Host "server listening on 127.0.0.1:$port (task '$taskName', log build\mcp_public.log)"
} else {
    throw "the server did not come up on port $port; see build\mcp_public.log"
}

# 3. the funnel
& $tailscale funnel --bg $port | Out-Null
$status = & $tailscale status --json | ConvertFrom-Json
$dns = $status.Self.DNSName.TrimEnd('.')

# 4. the URL
Write-Host ""
Write-Host "Give friends this URL (Claude Desktop / claude.ai -> Settings -> Connectors -> Add custom connector):"
Write-Host "  https://$dns/t/$token/mcp"
Write-Host ""
Write-Host "Or, for Claude Code:"
Write-Host "  claude mcp add --transport http wotr https://$dns/mcp --header `"Authorization: Bearer $token`""

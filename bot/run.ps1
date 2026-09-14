# Runs WOTR Bot and restarts it if it dies. Registered as the scheduled task "WOTR bot" (at logon).
#   powershell -ExecutionPolicy Bypass -File bot\run.ps1 [-Sync]
param([switch]$Sync)
$root = Split-Path $PSScriptRoot -Parent
$log = Join-Path $PSScriptRoot ".bot.log"
$env:PYTHONIOENCODING = "utf-8"
$args = @("$PSScriptRoot\main.py"); if ($Sync) { $args += "--sync" }
while ($true) {
    "$(Get-Date -Format s) starting" | Out-File -Append -Encoding utf8 $log
    & python @args 2>&1 | Out-File -Append -Encoding utf8 $log
    "$(Get-Date -Format s) exited ($LASTEXITCODE); restarting in 30s" | Out-File -Append -Encoding utf8 $log
    Start-Sleep -Seconds 30
}

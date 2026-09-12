# Register WOTR MCP with Claude Desktop.
#
# Claude Desktop rewrites claude_desktop_config.json from memory whenever it
# starts, so the entry has to be added while the app is closed. This script
# quits Claude, patches the config, and relaunches it. Run it from a PowerShell
# window OUTSIDE Claude (Start -> "PowerShell"):
#
#   powershell -ExecutionPolicy Bypass -File C:\Users\isaac\Documents\wotr-rule-index\build\install_mcp.ps1

$ErrorActionPreference = "Stop"
$cfgPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$repo = Split-Path -Parent $PSScriptRoot
$python = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
if (-not (Test-Path $python)) { $python = (Get-Command python).Source }

# 1. quit Claude Desktop and remember where it lives
$claude = Get-Process -Name Claude -ErrorAction SilentlyContinue | Select-Object -First 1
$exe = if ($claude) { $claude.Path } else { "$env:LOCALAPPDATA\AnthropicClaude\claude.exe" }
if ($claude) {
    Write-Host "Quitting Claude Desktop..."
    Get-Process -Name Claude -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 4
}

# 2. add the server entry
Copy-Item $cfgPath "$cfgPath.bak" -Force
$cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
if (-not $cfg.mcpServers) { $cfg | Add-Member -NotePropertyName mcpServers -NotePropertyValue ([pscustomobject]@{}) }
$entry = [pscustomobject]@{
    command = $python
    args    = @("$repo\build\mcp_server.py")
}
$cfg.mcpServers | Add-Member -NotePropertyName "WOTR MCP" -NotePropertyValue $entry -Force
$json = $cfg | ConvertTo-Json -Depth 30
[IO.File]::WriteAllText($cfgPath, $json, (New-Object Text.UTF8Encoding $false))
Write-Host "Added 'WOTR MCP' -> $python $repo\build\mcp_server.py"

# 3. relaunch
if (Test-Path $exe) {
    Start-Process $exe
    Write-Host "Claude Desktop relaunched. WOTR MCP appears in the tools menu inside a chat."
} else {
    Write-Host "Config written. Start Claude Desktop from the Start menu."
}

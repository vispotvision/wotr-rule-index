# Weekly backup of the canon to Google Drive (see build/backup.py). Registered as the
# scheduled task "WOTR weekly backup" (Sunday 03:00).
#   powershell -ExecutionPolicy Bypass -File build\backup.ps1
$ErrorActionPreference = "Continue"
$repo = Split-Path -Parent $PSScriptRoot
Set-Location $repo
$python = "C:\Users\isaac\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"
if (-not (Test-Path $python)) { $python = (Get-Command python).Source }
$env:PYTHONIOENCODING = "utf-8"
& $python build\backup.py 2>&1 | ForEach-Object { "$_" }

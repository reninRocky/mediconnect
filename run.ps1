$ErrorActionPreference = "Stop"

Set-Location "$PSScriptRoot"

if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
  Write-Host "Virtual environment not found. Run .\setup-windows.ps1 first."
  exit 1
}

. .\venv\Scripts\Activate.ps1
python app.py

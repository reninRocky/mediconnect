$ErrorActionPreference = "Stop"

Write-Host "== MediConnect setup (Windows) =="
Set-Location "$PSScriptRoot"

function Get-PythonCmd {
  if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
  if (Get-Command py -ErrorAction SilentlyContinue) { return "py" }
  throw "Python not found. Install Python 3.11+ and reopen the terminal."
}

$py = Get-PythonCmd

if (-not (Test-Path ".\venv")) {
  Write-Host "Creating virtual environment..."
  & $py -m venv venv
}

Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing requirements..."
pip install -r requirements.txt

if (-not (Test-Path ".\.env")) {
  Write-Host "Creating .env from .env.example..."
  Copy-Item ".\.env.example" ".\.env"
  Write-Host "Edit .env to set SECRET_KEY and GEMINI_API_KEY (optional)."
}

Write-Host "Done."

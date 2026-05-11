# ============================================================
# Asset Management Platform - One-click Start (PowerShell)
#   1. Backend : create venv, install deps, copy .env, run FastAPI
#   2. Frontend: npm install, run Vite dev server
#   3. Backend / Frontend run in their own new windows
# Usage:
#   Right click -> Run with PowerShell
#   or in PowerShell:   .\start.ps1
# ============================================================

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Backend = Join-Path $Root "Back_end"
$Frontend = Join-Path $Root "Front_end"

function Write-Step($msg) {
    Write-Host ""
    Write-Host "==> $msg" -ForegroundColor Cyan
}

function Test-Cmd($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

# ---------- env check ----------
Write-Step "Checking environment"
if (-not (Test-Cmd python)) {
    Write-Host "[X] python not found. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}
if (-not (Test-Cmd npm)) {
    Write-Host "[X] npm not found. Please install Node.js 18+." -ForegroundColor Red
    exit 1
}
$pyVer = (& python --version) 2>&1
$nodeVer = (& node --version) 2>&1
Write-Host "[OK] python : $pyVer"
Write-Host "[OK] node   : $nodeVer"

# ---------- backend prepare ----------
Write-Step "Preparing backend (Back_end)"
Push-Location $Backend
try {
    if (-not (Test-Path ".env")) {
        Write-Host "  - Copy .env.example -> .env"
        Copy-Item ".env.example" ".env"
        Write-Host "  ! Please edit Back_end\.env and set your MySQL user/password." -ForegroundColor Yellow
    }

    if (-not (Test-Path ".venv")) {
        Write-Host "  - Creating virtualenv .venv"
        & python -m venv .venv
    }

    Write-Host "  - Installing Python deps (skip if already up-to-date)"
    & ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt
}
finally {
    Pop-Location
}

# ---------- frontend prepare ----------
Write-Step "Preparing frontend (Front_end)"
Push-Location $Frontend
try {
    if (-not (Test-Path "node_modules")) {
        Write-Host "  - First run, executing npm install (this can take a while)"
        & npm install
    } else {
        Write-Host "  - node_modules exists, skip npm install"
    }
}
finally {
    Pop-Location
}

# ---------- launch ----------
Write-Step "Starting backend in a new window"
$backendCmd = "Set-Location '$Backend'; .\.venv\Scripts\Activate.ps1; python run.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd | Out-Null

Start-Sleep -Seconds 2

Write-Step "Starting frontend in a new window"
$frontendCmd = "Set-Location '$Frontend'; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd | Out-Null

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host " All started." -ForegroundColor Green
Write-Host "  Backend API : http://127.0.0.1:8000"
Write-Host "  API Docs    : http://127.0.0.1:8000/docs"
Write-Host "  Frontend    : http://localhost:5173"
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Tip: close those two new PowerShell windows to stop the services."

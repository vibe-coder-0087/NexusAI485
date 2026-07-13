# NexusAI local setup script (Windows PowerShell)
# Installs backend (Python) and frontend (Node) dependencies and creates .env files.
# Usage: run this from the project root (d:\Nexus AI\) in PowerShell.

Write-Host "==> Setting up NexusAI locally..." -ForegroundColor Cyan

# --- Backend ---
Write-Host "`n==> Backend: creating virtual environment" -ForegroundColor Cyan
Set-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "==> Backend: installing Python dependencies" -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "==> Created backend\.env from .env.example - fill in your API keys before running." -ForegroundColor Yellow
}

Set-Location ..

# --- Frontend ---
Write-Host "`n==> Frontend: installing Node dependencies" -ForegroundColor Cyan
Set-Location frontend
npm install

if (-Not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "==> Created frontend\.env from .env.example" -ForegroundColor Yellow
}

Set-Location ..

Write-Host "`n==> Setup complete." -ForegroundColor Green
Write-Host "To run locally (two terminals):"
Write-Host "  Backend : cd backend; .\venv\Scripts\Activate.ps1; python app.py"
Write-Host "  Frontend: cd frontend; npm run dev"

# Start backend + frontend together
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules\concurrently")) { npm install }
Write-Host "Starting RegionalClimate XAI (backend :5000 + frontend :3000)..." -ForegroundColor Cyan
npm run dev

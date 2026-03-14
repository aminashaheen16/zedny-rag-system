# 🚀 Zedny - Quick Start Script
# This script ensures clean startup of both frontend and backend

Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   ZEDNY ELITE - CLEAN STARTUP" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Step 1: Kill all existing backend instances
Write-Host "🔴 [1/4] Stopping all backend instances..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*app.main*"
} | Stop-Process -Force
Start-Sleep -Seconds 2
Write-Host "✅ Backend instances stopped" -ForegroundColor Green
Write-Host ""

# Step 2: Verify .env file exists
Write-Host "🔍 [2/4] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file found" -ForegroundColor Green
}
else {
    Write-Host "⚠️  WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "   Please create .env with required API keys" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 3: Start backend
Write-Host "🚀 [3/4] Starting backend on port 8000..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "py -m uvicorn app.main:app --reload --port 8000"
Start-Sleep -Seconds 3
Write-Host "✅ Backend started" -ForegroundColor Green
Write-Host ""

# Step 4: Instructions for frontend
Write-Host "📱 [4/4] Frontend Instructions:" -ForegroundColor Yellow
Write-Host "   Open a NEW terminal in the project root and run:" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host ""

Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   ✅ SETUP COMPLETE" -ForegroundColor Green
Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access Points:" -ForegroundColor White
Write-Host "  • Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  • API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  • Frontend:    http://localhost:5173 (after npm run dev)" -ForegroundColor Cyan
Write-Host ""

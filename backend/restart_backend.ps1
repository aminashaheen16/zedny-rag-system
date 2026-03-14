# Kill all Python processes running uvicorn
Write-Host "🔴 Stopping all backend instances..." -ForegroundColor Red
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*uvicorn*"} | Stop-Process -Force

Start-Sleep -Seconds 2

Write-Host "✅ All instances stopped. Starting fresh backend..." -ForegroundColor Green
py -m uvicorn app.main:app --reload --port 8000

# Local Docker Test Script (PowerShell)
# This script builds and tests the Docker container locally

Write-Host "🐳 Building Docker image locally..." -ForegroundColor Green
docker build -t it-helpdesk:test .

Write-Host "🧪 Testing Docker container..." -ForegroundColor Yellow
Write-Host "Starting container on port 8501..." -ForegroundColor Yellow
docker run -d --name it-helpdesk-test -p 8501:8501 `
  -e GROK_API_KEY="test-key" `
  -e JWT_SECRET_KEY="test-secret-key" `
  it-helpdesk:test

Write-Host "⏳ Waiting for container to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "🔍 Checking container health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501/_stcore/health" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Container is healthy!" -ForegroundColor Green
        Write-Host "🌐 Access the app at: http://localhost:8501" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ Container health check failed" -ForegroundColor Red
    Write-Host "📋 Container logs:" -ForegroundColor Yellow
    docker logs it-helpdesk-test
}

Write-Host ""
Write-Host "🛑 To stop the test container:" -ForegroundColor Cyan
Write-Host "docker stop it-helpdesk-test; docker rm it-helpdesk-test"

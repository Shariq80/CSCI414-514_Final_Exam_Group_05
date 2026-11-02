
$ApiContainer = "api_server"
$ClientContainer = "game_client"
$ApiUrl = "http://192.168.145.10:8000/health"

Write-Host "=================================="
Write-Host "API AUTOMATION AND RECOVERY"
Write-Host "=================================="

Write-Host "[1] Checking API health..."

docker exec $ClientContainer python3 -c "import urllib.request; urllib.request.urlopen('$ApiUrl', timeout=5)" 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "API is healthy. No recovery needed."
    exit 0
}

Write-Host "API is unavailable."
Write-Host "[2] Restarting Uvicorn..."

docker exec $ApiContainer pkill -x uvicorn

Start-Sleep -Seconds 2

docker exec -d $ApiContainer uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir /

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Could not start Uvicorn."
    exit 1
}

Write-Host "[3] Waiting for API recovery..."

for ($attempt = 1; $attempt -le 10; $attempt++) {
    Start-Sleep -Seconds 2

    docker exec $ClientContainer python3 -c "import urllib.request; urllib.request.urlopen('$ApiUrl', timeout=5)" 2>$null

    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: API recovered."
        docker exec $ClientContainer python3 -c "import urllib.request; print(urllib.request.urlopen('$ApiUrl').read().decode())"
        exit 0
    }

    Write-Host "Waiting... attempt $attempt/10"
}

Write-Host "ERROR: API recovery failed."
exit 1

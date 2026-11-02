
#!/bin/bash

API_CONTAINER="api_server"
CLIENT_CONTAINER="game_client"
API_URL="http://192.168.145.10:8000/health"

echo "=================================="
echo "API AUTOMATION AND RECOVERY"
echo "=================================="

echo "[1] Checking API health..."

if docker exec "$CLIENT_CONTAINER" python3 -c "import urllib.request; urllib.request.urlopen('$API_URL', timeout=5)" 2>/dev/null; then
    echo "API is healthy."
    exit 0
fi

echo "API is unavailable."
echo "[2] Attempting to restart Uvicorn..."

docker exec "$API_CONTAINER" bash -c "pkill -f 'uvicorn main:app' || true"

sleep 2

docker exec -d "$API_CONTAINER" uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir /

echo "[3] Waiting for API to recover..."

for attempt in {1..10}; do
    sleep 2

    if docker exec "$CLIENT_CONTAINER" python3 -c "import urllib.request; urllib.request.urlopen('$API_URL', timeout=5)" 2>/dev/null; then
        echo "SUCCESS: API recovered."
        docker exec "$CLIENT_CONTAINER" python3 -c "import urllib.request; print(urllib.request.urlopen('$API_URL').read().decode())"
        exit 0
    fi

    echo "Waiting... attempt $attempt/10"
done

echo "ERROR: API recovery failed."
exit 1

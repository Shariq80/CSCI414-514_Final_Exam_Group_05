# Automation and Recovery Report

## 1. Overview

This report demonstrates automated health checking, failure detection, and recovery for the Multiplayer Game State Service.

The test intentionally stopped the Uvicorn API process while keeping the Docker container and Redis database running. A PowerShell recovery script detected the failure, restarted the API process, and verified that the service was healthy again.

## 2. Test Environment

- Application: Multiplayer Game State Service
- API Framework: FastAPI
- API Server Container: `api_server`
- Client Container: `game_client`
- Database: Redis (`nosql_db`)
- Automation Script: `recovery.ps1`
- Operating System: Windows with Docker Desktop

## 3. Automation

The `recovery.ps1` script performs the following operations:

1. Checks the API health endpoint.
2. Detects when the API is unavailable.
3. Stops any existing Uvicorn process.
4. Starts Uvicorn again inside the API container.
5. Waits for the API to become available.
6. Performs another health check.
7. Reports whether recovery succeeded or failed.

The script can also confirm that the API is already healthy without restarting it.

## 4. Failure Simulation

To simulate an API failure, the Uvicorn process was stopped using:

`docker exec api_server pkill -x uvicorn`

The process check confirmed that Uvicorn was no longer running.

A health check from the game client returned:

`ConnectionRefusedError: [Errno 111] Connection refused`

The API container remained running during this test. The Redis database was not stopped.

## 5. Automated Recovery

The recovery script was executed using:

`powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\recovery.ps1`

The script detected the unavailable API and restarted Uvicorn automatically.

The recovery output confirmed:

`SUCCESS: API recovered.`

The final health check returned:

`{"status":"healthy","database":"connected"}`

## 6. Recovery Verification

After recovery, the following checks were performed:

| Verification | Result |
|---|---|
| Uvicorn process running | Passed |
| API reachable from game_client | Passed |
| API health endpoint | Passed |
| Redis database connection | Passed |
| Automated recovery | Passed |

The restarted Uvicorn process was confirmed with PID `4277`.

## 7. Conclusion

The automation and recovery test successfully demonstrated that the API service can recover from a process failure without restarting the entire Docker container.

The PowerShell script detected the failure, restarted the API process, and verified that the API and Redis connection were healthy again.

This provides a basic automated recovery mechanism for the Multiplayer Game State Service.

## 8. Evidence

Screenshots are saved in the `Test_Evidence` folder:

- `Recovery_Before_Failure.png`
- `Recovery_API_Failure.png`
- `Recovery_Automatic_Restart.png`

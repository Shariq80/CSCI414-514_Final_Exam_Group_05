This document provides a step-by-step guide to deploying and testing our isolated multi-subnet architecture for Multiplayer Game State Service. Follow these standard operations to replicate the baseline and run the high-volume simulation test.

1. Required Directory File Layout
Before beginning, ensure you have a dedicated project folder on your host machine containing these three files:
• docker-compose.yml (Handles our isolated subnets and node definitions)
• main.py (The FastAPI application backend script)
• simulate.py (The 1,050 record client simulation script backed by the OpenDota API)

2. Deploying the Environment Containers
    1. Clear Port/Network Conflicts (WSL/Windows Only):
        If you experience persistent network binding locks or switch failures from previous runs, execute this command inside an administrative PowerShell terminal on your host machine:
        ```powershell
        netsh int ip reset; wsl --shutdown
        ```
    2. Spin Up the Infrastructure Stack: Launch the core networks and container nodes in detached background mode:
        ```bash
        docker compose up -d
        ```
    3. Verify Container Node Status: Check that all four required network elements are actively running and healthy:
        ```bash
        docker compose ps
        ```
3. Module A: Network Infrastructure Verification
    1. Client Routing: Verify that the default gateway forces traffic out through our dedicated router node instead of standard Docker shortcuts:
        ```bash
        docker exec -it game_client ip route
        ```
        Ensure the output explicitly displays default via 192.168.144.254.
    2. Multi-Subnet Path Verification: Confirm that traffic headed toward the database tier travels across the central network router boundaries:
        ```bash
        docker exec -it game_client traceroute -n 192.168.146.10
        ```
        Verify that Hop 1 explicitly lists our router gateway interface IP 192.168.144.254 before hitting the database on Hop 2.

4. Module B: Distributed API & Database Integration
Deploy our active application services and trigger the heavy-workload pipeline simulation:
    1. Initialize the Backend API Gateway: Copy the server configuration file into the application container and start the background Uvicorn routing loop:
        ```bash
        docker cp main.py api_server:/app/main.py
        docker exec -d api_server bash -c "cd /app && uvicorn main:app --host 0.0.0.0 --port 8000
        ```
    2. Execute the High-Volume Data Stream: Copy the simulation script over to the client container node and run the test suite to push 1,050 telemetry operations across the network:
        ```bash
        docker cp simulate.py game_client:/simulate.py
        docker exec -it game_client python3 /simulate.py
        ```
    3. Audit Persistent Storage Registration: Verify that every packet sent over the network successfully registered inside the non-volatile database zone:
        ```bash
        docker exec -it nosql_db redis-cli DBSIZE
        ```
        The terminal output must display exactly (integer) 1050, aligning perfectly with our script metrics.

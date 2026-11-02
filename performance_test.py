import requests
import time
import statistics

API_URL = "http://192.168.145.10:8000"
TOTAL_REQUESTS = 1050

response_times = []
success_count = 0
failure_count = 0

print("Starting Performance Test...")
print(f"Total requests: {TOTAL_REQUESTS}")
print("Network condition: Normal (Baseline)")
print("-" * 45)

test_start = time.perf_counter()

for i in range(1, TOTAL_REQUESTS + 1):
    payload = {
        "player_id": f"performance_player_{i}",
        "match_id": f"performance_match_{i % 100}",
        "x_pos": float(i * 1.5),
        "y_pos": float(i * 2.5),
        "score": i * 10
    }

    request_start = time.perf_counter()

    try:
        response = requests.post(
            f"{API_URL}/update_state",
            json=payload,
            timeout=5
        )

        request_end = time.perf_counter()
        latency = (request_end - request_start) * 1000

        response_times.append(latency)

        if response.status_code == 200:
            success_count += 1
        else:
            failure_count += 1

    except requests.RequestException as error:
        failure_count += 1
        print(f"Request {i} failed: {error}")

    if i % 200 == 0:
        print(f"Completed {i}/{TOTAL_REQUESTS} requests")

total_time = time.perf_counter() - test_start

if response_times:
    average_latency = statistics.mean(response_times)
    median_latency = statistics.median(response_times)
    sorted_times = sorted(response_times)
    p95_index = int(0.95 * (len(sorted_times) - 1))
    p95_latency = sorted_times[p95_index]
    throughput = success_count / total_time
    success_rate = (success_count / TOTAL_REQUESTS) * 100

    print("\n========== PERFORMANCE RESULTS ==========")
    print(f"Successful requests: {success_count}")
    print(f"Failed requests: {failure_count}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average latency: {average_latency:.2f} ms")
    print(f"Median latency: {median_latency:.2f} ms")
    print(f"95th percentile latency: {p95_latency:.2f} ms")
    print(f"Total execution time: {total_time:.2f} seconds")
    print(f"Throughput: {throughput:.2f} requests/second")
    print("==========================================")
else:
    print("No successful HTTP responses. Check API connectivity.")

# Performance Testing Report

## 1. Overview

This report evaluates the performance of the Multiplayer Game State Service under normal network conditions and simulated network impairment.

The purpose of the testing was to measure request latency, throughput, and reliability when communicating with the API server.

## 2. Test Environment

- **Application:** Multiplayer Game State Service
- **API Server:** FastAPI
- **Database:** Redis
- **Testing Client:** game_client Docker container
- **Total Requests:** 1,050 per test
- **Request Type:** POST `/update_state`
- **Testing Tool:** Python with the Requests library

## 3. Baseline Performance Test

The first test was performed under normal network conditions without additional network delay or packet loss.

| Metric | Result |
|---|---:|
| Total Requests | 1,050 |
| Successful Requests | 1,050 |
| Failed Requests | 0 |
| Success Rate | 100% |
| Average Latency | 4.90 ms |
| Median Latency | 4.69 ms |
| P95 Latency | 6.04 ms |
| Total Execution Time | 5.15 seconds |
| Throughput | 203.75 requests/second |

## 4. Network Impairment Test

The second test used Linux Traffic Control (`tc`) with the NetEm module to simulate network problems on the game client's outgoing network interface.

The following conditions were applied:

- Added delay: 100 ms
- Delay variation: 10 ms
- Packet loss: 1%

The same performance test script and 1,050 POST requests were used.

| Metric | Result |
|---|---:|
| Total Requests | 1,050 |
| Successful Requests | 1,050 |
| Failed Requests | 0 |
| Success Rate | 100% |
| Average Latency | 232.75 ms |
| Median Latency | 210.46 ms |
| P95 Latency | 224.87 ms |
| Total Execution Time | 244.40 seconds |
| Throughput | 4.30 requests/second |

## 5. Performance Comparison

| Metric | Baseline | Network Impairment |
|---|---:|---:|
| Average Latency | 4.90 ms | 232.75 ms |
| Median Latency | 4.69 ms | 210.46 ms |
| P95 Latency | 6.04 ms | 224.87 ms |
| Throughput | 203.75 req/sec | 4.30 req/sec |
| Success Rate | 100% | 100% |

## 6. Analysis

The results show that network conditions have a significant impact on application performance.

Under normal conditions, the service processed 1,050 requests with an average latency of 4.90 ms and throughput of 203.75 requests per second.

After adding network delay and packet loss, average latency increased to 232.75 ms, while throughput decreased to 4.30 requests per second.

Despite the slower performance, all 1,050 requests succeeded in both tests. This suggests that the service was able to complete the requests under the tested network conditions, although response times were much slower.

TCP retransmission can help recover from packet loss, which may explain why packet loss did not result in failed HTTP requests during this test.

## 7. Conclusion

The performance tests successfully demonstrated how network impairment affects the Multiplayer Game State Service.

The application maintained a 100% request success rate in both tests. However, additional network delay and packet loss significantly increased latency and reduced throughput.

These results provide a baseline for evaluating future performance improvements and testing the system under different network conditions.

## 8. Evidence

Screenshots are saved in the `Test_Evidence` folder:

- `Performance_Baseline.png`
- `Performance_Network_Impairment.png`
- `Client_Routing_Verification.png`

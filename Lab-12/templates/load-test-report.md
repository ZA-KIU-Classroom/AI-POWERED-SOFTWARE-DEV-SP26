# Load Test Report

Commit this to your repo at `load/load-test-report.md`. Screenshot the Locust summary and reference it here. Measurements are 25 percent of the Demo Day rubric.

## Configuration

- Target host: `https://__________.up.railway.app`
- Users: ______   Spawn rate: ______   Duration: ______
- Primary model under test: ______________________
- Date and time of run: ______________________

## Results

| Metric | Result | Target | Pass? |
|---|---|---|---|
| `/health` response time | ______ ms | under 500ms | |
| Chat p50 latency | ______ ms | reference | |
| Chat p95 latency | ______ ms | under 2000ms | |
| Chat p99 latency | ______ ms | reference | |
| Throughput | ______ req/s | reference | |
| Error rate | ______ % | under 2% | |
| 429 / fallback events | ______ | fallback should catch | |

## What broke first

Describe the first thing to degrade as load increased (cold start, rate limit, latency, cost).

> 

## What you changed in response

> 

## Cost note

Approximate token spend for this run, and projected monthly cost at expected usage.

> 

_Screenshot: `load/screenshots/locust-summary.png`_

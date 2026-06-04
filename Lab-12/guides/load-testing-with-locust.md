# Guide · Load Testing with Locust

Load testing sends many requests at once so you discover your breaking point before the Demo Day audience does. You are not chasing a perfect score. You are learning your real numbers and confirming your fallback chain fires under pressure.

## 1. Install

```bash
pip install locust
locust --version
```

## 2. Get the starter file

Copy `examples/locustfile.py` into a new `load/` folder in your repo:

```bash
mkdir -p load
cp /path/to/Lab-12/examples/locustfile.py load/locustfile.py
```

Open it and change one thing: nothing. The host is passed on the command line, and the endpoint path defaults to `/api/chat`. If your chat route is different, edit the `@task` method.

## 3. Run a load test

```bash
locust -f load/locustfile.py \
  --host https://your-app.up.railway.app \
  --users 50 --spawn-rate 10 --run-time 2m --headless
```

- `--users 50` simulates 50 concurrent users, roughly your whole class hitting at once.
- `--spawn-rate 10` adds 10 users per second until it reaches 50.
- `--run-time 2m` runs for two minutes, then stops.
- `--headless` runs in the terminal. Drop it to get the web dashboard at `http://localhost:8089`.

## 4. Read the results

Locust prints a summary table. The columns that matter:

| Column | What it tells you |
|---|---|
| `# reqs` | total requests sent |
| `# fails` | failed requests. Your error rate is fails divided by reqs |
| `Median (ms)` | your p50, the typical user experience |
| `95%ile (ms)` | your p95, the unlucky user. This is the number to watch |
| `99%ile (ms)` | your p99, the worst case |
| `req/s` | throughput your app sustained |

## 5. The targets for Demo Day

| Metric | Target |
|---|---|
| `/health` response | under 500ms (a Repository Review hard gate) |
| Chat p95 latency | under 2000ms |
| Error rate | under 2% at class-wide concurrency |
| Fallback | fires on a 429, user still gets a working answer |

## 6. Confirm your fallback actually fires

This is the most important test. While the load test runs, your primary provider may return 429 rate-limit errors. Watch your application logs: you should see the fallback chain activate and `model_used` switch to your secondary or OSS model. If instead you see errors reaching users, your fallback is not wired correctly. Fix that before Demo Day, because the room hitting you at once is exactly when it matters.

## 7. Be kind to your budget

Concurrency multiplies token spend. Run your first pass against a cheap model (Gemini Flash or Qwen 3.5 via OpenRouter) to confirm the script works, then run one short two-minute pass against your real primary so the numbers are honest. Do not leave a 50-user test running against an expensive model.

## 8. Record it

Fill in `templates/load-test-report.md`, screenshot the Locust summary into `load/screenshots/`, and commit both. That screenshot is your evidence on the measurements slide.

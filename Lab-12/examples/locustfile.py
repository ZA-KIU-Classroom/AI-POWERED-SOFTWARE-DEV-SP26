"""
Locust load test for your CS-AI-2025 capstone.

Copy this to your repo as load/locustfile.py, then run:

    locust -f load/locustfile.py \
        --host https://your-app.up.railway.app \
        --users 50 --spawn-rate 10 --run-time 2m --headless

Drop --headless to open the web dashboard at http://localhost:8089.

This test exercises two endpoints:
  - GET  /health    should respond under 500ms (a Repository Review gate)
  - POST /api/chat  your main chat route, checked against a 2s p95 target

Adjust the path or payload in the @task methods if your routes differ.
"""

from locust import HttpUser, task, between

# A small set of realistic prompts so every request is not identical.
PROMPTS = [
    "Summarise this document in three sentences.",
    "What are the key risks in this proposal?",
    "Explain the main idea simply.",
    "List three action items from this text.",
]


class CapstoneUser(HttpUser):
    # Each simulated user waits 1 to 3 seconds between requests,
    # which is closer to real human pacing than hammering with no pause.
    wait_time = between(1, 3)

    # Cycle through prompts so we do not just test a cached single answer.
    _i = 0

    @task(1)
    def health(self):
        """Health check should be fast. Flag anything over 500ms."""
        with self.client.get("/health", catch_response=True) as res:
            if res.elapsed.total_seconds() > 0.5:
                res.failure("health slower than 500ms")
            elif res.status_code != 200:
                res.failure(f"health status {res.status_code}")

    @task(5)
    def chat(self):
        """Main chat path. The 5:1 weight means chat is hit far more
        often than health, which mirrors real traffic."""
        prompt = PROMPTS[CapstoneUser._i % len(PROMPTS)]
        CapstoneUser._i += 1

        with self.client.post(
            "/api/chat",
            json={"message": prompt},
            catch_response=True,
        ) as res:
            # A 429 means your primary provider rate-limited you.
            # Your fallback chain from Lab 11 should have caught this,
            # so the user still gets a 200. A 429 reaching here is a bug.
            if res.status_code == 429:
                res.failure("429: fallback chain did not catch the rate limit")
            elif res.status_code != 200:
                res.failure(f"chat status {res.status_code}")
            elif res.elapsed.total_seconds() > 2.0:
                res.failure("chat slower than 2s (p95 target)")
            else:
                # Optional: confirm the response shape your app returns.
                try:
                    body = res.json()
                    if not body.get("answer"):
                        res.failure("200 but no answer field in response")
                except Exception:
                    res.failure("200 but response was not valid JSON")

"""
rate_limiter.py
Token bucket rate limiter for FastAPI.

Place this file in your backend/ directory alongside main.py.
See usage_example.py for how to wire it into your endpoints.

How the token bucket works:
  - Each user starts with MAX_TOKENS tokens in their bucket.
  - Each request costs 1 token.
  - Tokens refill at REFILL_RATE per minute, continuously.
  - When the bucket is empty, the request is rejected with HTTP 429.
  - The bucket is stored in memory. It resets if the server restarts.
    For production persistence, replace the dict with Redis.
"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException


# ── Configuration ─────────────────────────────────────────────────────────────
# Adjust these values to match your application's usage patterns.

REFILL_RATE = 10    # Tokens restored per minute. 10 = one request per 6 seconds sustained.
MAX_TOKENS  = 10    # Maximum burst size. A user can send 10 rapid requests, then slows down.
SESSION_LIMIT = 50  # Maximum requests per session total. Prevents runaway sessions.


# ── Bucket storage ────────────────────────────────────────────────────────────
# In-memory. Resets on server restart.
# Replace with Redis for persistence across restarts and horizontal scaling.

_BUCKETS: dict = defaultdict(lambda: {
    "tokens": float(MAX_TOKENS),
    "last_refill": time.time(),
    "total_requests": 0,
})


# ── Core function ─────────────────────────────────────────────────────────────

def check_rate_limit(user_id: str) -> None:
    """
    Check whether the user has remaining tokens.
    Raises HTTPException(429) if the bucket is empty or the session limit is reached.
    Call this at the start of any endpoint that makes LLM calls.

    Args:
        user_id: A string identifying the user. Use a session token, user ID,
                 or fall back to the client IP address. Do not use "anon" for
                 all users — that creates a single shared bucket for everyone.
    """
    bucket = _BUCKETS[user_id]
    now = time.time()

    # Refill tokens based on time elapsed since last request.
    elapsed_minutes = (now - bucket["last_refill"]) / 60.0
    refill_amount = elapsed_minutes * REFILL_RATE
    bucket["tokens"] = min(float(MAX_TOKENS), bucket["tokens"] + refill_amount)
    bucket["last_refill"] = now

    # Check session limit.
    if bucket["total_requests"] >= SESSION_LIMIT:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "session_limit_exceeded",
                "message": (
                    "You have reached the maximum number of requests for this session. "
                    "Start a new session to continue."
                ),
                "session_limit": SESSION_LIMIT,
                "requests_made": bucket["total_requests"],
            },
        )

    # Check token bucket.
    if bucket["tokens"] < 1.0:
        # Calculate how many seconds until one token refills.
        seconds_until_refill = (1.0 - bucket["tokens"]) / (REFILL_RATE / 60.0)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "You are sending requests too quickly. Please wait before trying again.",
                "retry_after_seconds": round(seconds_until_refill, 1),
                "requests_per_minute": REFILL_RATE,
            },
        )

    # Consume one token and record the request.
    bucket["tokens"] -= 1.0
    bucket["total_requests"] += 1


def get_bucket_status(user_id: str) -> dict:
    """
    Return the current state of a user's bucket.
    Useful for debugging and for surfacing rate limit state in your frontend.
    """
    bucket = _BUCKETS.get(user_id)
    if not bucket:
        return {
            "user_id": user_id,
            "tokens_remaining": MAX_TOKENS,
            "total_requests": 0,
            "session_limit": SESSION_LIMIT,
        }
    return {
        "user_id": user_id,
        "tokens_remaining": round(bucket["tokens"], 2),
        "total_requests": bucket["total_requests"],
        "session_limit": SESSION_LIMIT,
        "requests_until_session_limit": max(0, SESSION_LIMIT - bucket["total_requests"]),
    }

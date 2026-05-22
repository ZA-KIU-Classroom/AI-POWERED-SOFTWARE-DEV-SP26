"""
usage_example.py
Shows how to wire rate_limiter.py into your FastAPI chat endpoint.

This is a reference file. Do not import it directly.
Copy the relevant lines into your existing main.py.

Lines marked ADD are the three additions you make to your existing code.
Everything else is your existing code shown for context.
"""

import os
import time
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

# ADD: import the rate limiter
from rate_limiter import check_rate_limit, get_bucket_status

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []


# ── Your existing chat endpoint, with rate limiting added ─────────────────────

@app.post("/api/ai/chat")
async def chat(request: Request, body: ChatRequest):
    # ADD 1: Extract a user identifier from the request.
    # X-User-ID is a custom header your frontend should send.
    # Fall back to the client IP address if the header is absent.
    # Do not use "anon" for all users — that creates one shared bucket.
    user_id = request.headers.get("X-User-ID") or request.client.host

    # ADD 2: Check the rate limit. Raises HTTP 429 automatically if exceeded.
    # This must come before any LLM calls.
    check_rate_limit(user_id)

    # Your existing logic below — do not change this part.
    # -------------------------------------------------------------------------
    try:
        # ... your OpenRouter call goes here ...
        response_text = "This is a placeholder response."

        # Log to episode log as you normally would.
        return {
            "response": response_text,
            "conversation_history": body.conversation_history + [
                {"role": "user", "content": body.message},
                {"role": "assistant", "content": response_text},
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Optional: expose bucket status for debugging ──────────────────────────────

@app.get("/api/rate-limit/status")
async def rate_limit_status(request: Request):
    """
    Returns the current rate limit status for the requesting user.
    Useful for your frontend to show a usage indicator.
    Remove this endpoint before Demo Day if you do not want it public.
    """
    user_id = request.headers.get("X-User-ID") or request.client.host
    return get_bucket_status(user_id)


# ── How to test the rate limiter manually ────────────────────────────────────
#
# Start your app: uvicorn main:app --reload
#
# Then in a separate terminal, send 15 rapid requests:
#
#   for i in {1..15}; do
#     curl -s -o /dev/null -w "%{http_code}\n" \
#       -X POST http://localhost:8000/api/ai/chat \
#       -H "Content-Type: application/json" \
#       -H "X-User-ID: test-user-123" \
#       -d '{"message": "test", "conversation_history": []}';
#   done
#
# Expected output: ten 200s followed by five 429s.
#
# Check the 429 response body:
#
#   curl -X POST http://localhost:8000/api/ai/chat \
#     -H "Content-Type: application/json" \
#     -H "X-User-ID: test-user-123" \
#     -d '{"message": "test", "conversation_history": []}'
#
# Expected body:
#   {
#     "detail": {
#       "error": "rate_limit_exceeded",
#       "message": "You are sending requests too quickly...",
#       "retry_after_seconds": 5.8,
#       "requests_per_minute": 10
#     }
#   }

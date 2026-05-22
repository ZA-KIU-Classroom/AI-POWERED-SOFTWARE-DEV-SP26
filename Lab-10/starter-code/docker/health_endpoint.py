"""
health_endpoint.py
Drop-in /health and /health/deep endpoints for FastAPI.

Copy the imports and the two route functions into your main.py.
Do not copy the app = FastAPI() line — you already have one.

IMPORTANT: The /health endpoint must not call your LLM.
It must respond in under 100ms. If it is slow, Railway will
restart your container in a loop.
"""

import time
import os
from datetime import datetime, timezone
from fastapi import FastAPI

# Add these imports to your existing main.py imports
# import time
# from datetime import datetime, timezone

app = FastAPI()          # You already have this — do not duplicate it.
START_TIME = time.time() # Add this line near the top of main.py, after app = FastAPI()


@app.get("/health")
async def health():
    """
    Basic health check. Must respond in under 100ms.
    No external calls. No LLM calls. No database calls.
    Railway polls this every 30 seconds. If it fails 3 times in a row,
    the container is restarted.
    """
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - START_TIME),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
    }


@app.get("/health/deep")
async def health_deep():
    """
    Deep health check. Verifies that OpenRouter is reachable.
    Use this for your own debugging — do not expose it as the
    primary health endpoint because it makes an external call.

    This endpoint is optional. The /health endpoint above is what
    Railway, the grader, and Demo Day all use.
    """
    import httpx

    openrouter_key = os.getenv("OPENROUTER_API_KEY", "")
    if not openrouter_key:
        return {
            "status": "degraded",
            "openrouter": False,
            "error": "OPENROUTER_API_KEY not set",
        }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": "Bearer " + openrouter_key},
            )
        return {
            "status": "ok",
            "openrouter": response.status_code == 200,
            "openrouter_status": response.status_code,
        }
    except Exception as e:
        return {
            "status": "degraded",
            "openrouter": False,
            "error": str(e),
        }

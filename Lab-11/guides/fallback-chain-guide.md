# Guide: Implementing a Production Fallback Chain

This guide walks you through integrating a multi-model fallback chain into your existing FastAPI backend. Read it fully before you start coding. The implementation takes 30–45 minutes.

---

## What You Are Building

A function called `chat_with_fallback()` that:

1. Tries your PRIMARY model first
2. If that fails with a provider error (429, 5xx, timeout), logs the failure and tries SECONDARY
3. If SECONDARY also fails, tries OSS_FALLBACK
4. If all three fail, raises a clear error rather than hanging
5. Returns the result with a `model_used` field so your episode log knows which model answered

---

## Step 1 — Add model configuration to settings

Create or update `backend/settings.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Model configuration — all read from environment
# Never hardcode model names in your logic
PRIMARY_MODEL   = os.environ.get("PRIMARY_MODEL",   "anthropic/claude-sonnet-4-6")
SECONDARY_MODEL = os.environ.get("SECONDARY_MODEL", "google/gemini-3-flash")
OSS_FALLBACK    = os.environ.get("OSS_FALLBACK",    "qwen/qwen-3.5-32b")

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]  # Fail fast if missing

# Fallback chain — order matters
FALLBACK_CHAIN = [PRIMARY_MODEL, SECONDARY_MODEL, OSS_FALLBACK]

# Timeouts
LLM_TIMEOUT_SECONDS = 30.0
```

Confirm your `.env` and `.env.example` both contain:
```
PRIMARY_MODEL=anthropic/claude-sonnet-4-6
SECONDARY_MODEL=google/gemini-3-flash
OSS_FALLBACK=qwen/qwen-3.5-32b
```

---

## Step 2 — Add the fallback chain function

Create `backend/llm_client.py`:

```python
"""
llm_client.py — Production fallback chain for OpenRouter-routed models.

All models share the OpenAI-compatible interface via OpenRouter.
Change PRIMARY_MODEL in .env to switch providers without touching this file.
"""

import logging
import time
import openai

from backend.settings import (
    FALLBACK_CHAIN,
    OPENROUTER_API_KEY,
    LLM_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)

# One client — all models via OpenRouter
_client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def chat_with_fallback(
    messages: list[dict],
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> dict:
    """
    Send a chat request through the fallback chain.

    Tries each model in FALLBACK_CHAIN in order. Returns the first
    successful response. If all models fail, raises RuntimeError.

    Returns a dict with:
        content        (str)  — the model's response text
        model_used     (str)  — which model actually answered
        input_tokens   (int)  — tokens consumed by the prompt
        output_tokens  (int)  — tokens in the response
        latency_ms     (int)  — wall-clock milliseconds for this call
        fallback_used  (bool) — True if primary model was not used
    """
    last_error = None

    for model in FALLBACK_CHAIN:
        attempt_start = time.perf_counter()
        try:
            logger.info("LLM attempt: model=%s", model)

            response = _client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=LLM_TIMEOUT_SECONDS,
            )

            latency_ms = int((time.perf_counter() - attempt_start) * 1000)
            content = response.choices[0].message.content or ""

            logger.info(
                "LLM success: model=%s latency_ms=%d input=%d output=%d",
                model,
                latency_ms,
                response.usage.prompt_tokens,
                response.usage.completion_tokens,
            )

            return {
                "content":       content,
                "model_used":    model,
                "input_tokens":  response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "latency_ms":    latency_ms,
                "fallback_used": model != FALLBACK_CHAIN[0],
            }

        except openai.RateLimitError as e:
            # 429 — provider is throttling us, try next model
            logger.warning(
                "RateLimitError from model=%s: %s — trying next model",
                model, str(e)
            )
            last_error = e

        except openai.APIStatusError as e:
            # 5xx — provider-side error, try next model
            logger.warning(
                "APIStatusError status=%d from model=%s — trying next model",
                e.status_code, model
            )
            last_error = e

        except openai.APITimeoutError as e:
            # Request exceeded LLM_TIMEOUT_SECONDS
            logger.warning(
                "Timeout after %.0fs from model=%s — trying next model",
                LLM_TIMEOUT_SECONDS, model
            )
            last_error = e

        except openai.APIConnectionError as e:
            # Network-level failure
            logger.warning(
                "ConnectionError from model=%s: %s — trying next model",
                model, str(e)
            )
            last_error = e

    # All models exhausted
    logger.error(
        "All models in fallback chain exhausted. Last error: %s",
        str(last_error)
    )
    raise RuntimeError(
        f"All models exhausted after trying {len(FALLBACK_CHAIN)} providers. "
        f"Last error: {last_error}"
    )
```

---

## Step 3 — Update your chat endpoint to use the fallback chain

In `backend/main.py`, find your existing chat endpoint and replace the direct model call:

**Before (direct call — no fallback):**

```python
@app.post("/api/ai/chat")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4-6",  # hardcoded — bad
        messages=request.messages,
        max_tokens=1024,
    )
    return {"content": response.choices[0].message.content}
```

**After (fallback chain — portable):**

```python
from backend.llm_client import chat_with_fallback

@app.post("/api/ai/chat")
async def chat(request: ChatRequest):
    # check_rate_limit(request) — your existing rate limiter still runs
    
    result = chat_with_fallback(
        messages=request.messages,
        max_tokens=1024,
    )

    # Log to episode log — model_used is now recorded
    log_episode(
        user_message=request.messages[-1]["content"],
        assistant_message=result["content"],
        model_used=result["model_used"],
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        latency_ms=result["latency_ms"],
        fallback_used=result["fallback_used"],
    )

    return {
        "content":      result["content"],
        "model_used":   result["model_used"],  # expose to caller
        "latency_ms":   result["latency_ms"],
        "fallback_used": result["fallback_used"],
    }
```

The exact shape of your endpoint will differ — adapt it to your existing code. The key change is: call `chat_with_fallback()` instead of the direct client call, and include `model_used` in your response and episode log.

---

## Step 4 — Update your episode log schema

If your episode log is a JSON file, add these fields to each entry:

```python
def log_episode(
    user_message: str,
    assistant_message: str,
    model_used: str,       # NEW — which model answered
    input_tokens: int,
    output_tokens: int,
    latency_ms: int,
    fallback_used: bool,   # NEW — was primary model unavailable
    cache_read_tokens: int = 0,
    error_type: str | None = None,
):
    entry = {
        "timestamp":        datetime.utcnow().isoformat(),
        "user_message":     user_message[:200],   # truncate for log size
        "assistant_message": assistant_message[:500],
        "model_used":       model_used,           # NEW
        "fallback_used":    fallback_used,        # NEW
        "input_tokens":     input_tokens,
        "output_tokens":    output_tokens,
        "cache_read_tokens": cache_read_tokens,
        "latency_ms":       latency_ms,
        "error_type":       error_type,
    }
    # ... your existing append logic
```

---

## Step 5 — Test the fallback chain manually

This is the most important step. Verify it actually works before you commit.

```bash
# 1. Set PRIMARY_MODEL to something that does not exist
# In your .env:
PRIMARY_MODEL=this-model-does-not-exist

# 2. Restart your server
uvicorn backend.main:app --reload

# 3. Send a request
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'

# 4. Check your server logs — you should see:
# INFO  LLM attempt: model=this-model-does-not-exist
# WARNING  APIStatusError status=404 from model=this-model-does-not-exist — trying next model
# INFO  LLM attempt: model=google/gemini-3-flash
# INFO  LLM success: model=google/gemini-3-flash latency_ms=430 ...

# 5. Check the response — model_used should be google/gemini-3-flash
# {"content": "Hello! ...", "model_used": "google/gemini-3-flash", "fallback_used": true}

# 6. Restore PRIMARY_MODEL to your real model
```

Screenshot or copy the log output. Keep it as evidence — paste it into your model selection table notes or your commit message body.

---

## Step 6 — Restore your real PRIMARY_MODEL and restart

```bash
# Restore .env to real values
PRIMARY_MODEL=anthropic/claude-sonnet-4-6

# Restart server
uvicorn backend.main:app --reload

# Verify primary model is working again
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'
# model_used should be anthropic/claude-sonnet-4-6
```

---

## Common Mistakes to Avoid

**Catching bare `Exception` as the only handler**  
This hides bugs. Catch specific exception types. A `ValueError` from malformed input should not trigger a fallback to a different model — it should surface as a 400 error.

**Not restarting the server after changing `.env`**  
Environment variables are read at startup. If you change `.env` and do not restart, the server is still using the old values.

**Logging only the final result, not the attempts**  
Your instructor and the grader want to see evidence that the fallback chain ran. Log every attempt at `INFO` level, not just the final success.

**Returning a 500 error instead of using the fallback**  
The entire point of the chain is to avoid returning an error to the user when one model fails. If your endpoint returns 500 when the primary model returns 429, the fallback chain is not working.

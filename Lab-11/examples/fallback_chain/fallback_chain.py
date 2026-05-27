"""
examples/fallback_chain/fallback_chain.py

Production-ready fallback chain for multi-provider LLM routing.
Copy this file into your backend/ directory and integrate it with
your existing FastAPI application.

This is a standalone example you can run directly to verify it works
before integrating it into your capstone. See the integration guide
in guides/fallback-chain-guide.md.

Usage (standalone test):
    python examples/fallback_chain/fallback_chain.py

Usage (integrated):
    Copy to backend/llm_client.py and follow guides/fallback-chain-guide.md
"""

import logging
import os
import time
from typing import Optional

import openai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("llm_client")

# ── Configuration ─────────────────────────────────────────────────────────────

PRIMARY_MODEL    = os.environ.get("PRIMARY_MODEL",   "anthropic/claude-sonnet-4-6")
SECONDARY_MODEL  = os.environ.get("SECONDARY_MODEL", "google/gemini-3-flash")
OSS_FALLBACK     = os.environ.get("OSS_FALLBACK",    "qwen/qwen-3.5-32b")
OPENROUTER_KEY   = os.environ.get("OPENROUTER_API_KEY", "")
LLM_TIMEOUT      = float(os.environ.get("LLM_TIMEOUT_SECONDS", "30.0"))

FALLBACK_CHAIN   = [PRIMARY_MODEL, SECONDARY_MODEL, OSS_FALLBACK]

# ── Client ────────────────────────────────────────────────────────────────────

def _make_client() -> openai.OpenAI:
    if not OPENROUTER_KEY:
        raise EnvironmentError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to your .env file."
        )
    return openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
    )

_client: Optional[openai.OpenAI] = None

def get_client() -> openai.OpenAI:
    """Lazy-initialised singleton client."""
    global _client
    if _client is None:
        _client = _make_client()
    return _client

# ── Core function ─────────────────────────────────────────────────────────────

def chat_with_fallback(
    messages: list[dict],
    max_tokens: int = 1024,
    temperature: float = 0.7,
    system_prompt: Optional[str] = None,
) -> dict:
    """
    Send a chat request through the multi-model fallback chain.

    Args:
        messages:      List of {"role": "user"|"assistant", "content": str}
        max_tokens:    Maximum tokens in the response
        temperature:   Sampling temperature (0.0 = deterministic)
        system_prompt: Optional system message prepended to messages

    Returns:
        {
            "content":       str   — the model's response text
            "model_used":    str   — which model answered (e.g. "google/gemini-3-flash")
            "input_tokens":  int   — tokens consumed by the prompt
            "output_tokens": int   — tokens in the response
            "latency_ms":    int   — wall-clock milliseconds for this call
            "fallback_used": bool  — True if primary model was not used
        }

    Raises:
        RuntimeError: if all models in FALLBACK_CHAIN are exhausted
    """
    client = get_client()

    # Prepend system message if provided
    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    last_error = None

    for model in FALLBACK_CHAIN:
        attempt_start = time.perf_counter()

        try:
            logger.info("Attempting model=%s", model)

            response = client.chat.completions.create(
                model=model,
                messages=full_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=LLM_TIMEOUT,
            )

            latency_ms = int((time.perf_counter() - attempt_start) * 1000)
            content    = response.choices[0].message.content or ""

            if not content.strip():
                # Empty response — treat as a soft failure and try next model
                logger.warning(
                    "Empty response from model=%s — trying next model", model
                )
                last_error = ValueError(f"Empty response from {model}")
                continue

            logger.info(
                "Success: model=%s latency_ms=%d input=%d output=%d",
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
            logger.warning(
                "RateLimitError (429) from model=%s — trying next model. error=%s",
                model, str(e)[:100],
            )
            last_error = e

        except openai.APIStatusError as e:
            logger.warning(
                "APIStatusError status=%d from model=%s — trying next model",
                e.status_code, model,
            )
            last_error = e

        except openai.APITimeoutError:
            logger.warning(
                "Timeout (%.0fs) from model=%s — trying next model",
                LLM_TIMEOUT, model,
            )
            last_error = TimeoutError(f"Model {model} timed out after {LLM_TIMEOUT}s")

        except openai.APIConnectionError as e:
            logger.warning(
                "ConnectionError from model=%s — trying next model. error=%s",
                model, str(e)[:100],
            )
            last_error = e

    # All models exhausted
    logger.error(
        "All %d models in fallback chain exhausted. Last error: %s",
        len(FALLBACK_CHAIN), str(last_error),
    )
    raise RuntimeError(
        f"All models exhausted after trying {len(FALLBACK_CHAIN)} providers. "
        f"Chain: {' > '.join(FALLBACK_CHAIN)}. "
        f"Last error: {last_error}"
    )

# ── FastAPI integration example ───────────────────────────────────────────────

"""
To integrate with your existing FastAPI app, update your chat endpoint like this:

    from backend.llm_client import chat_with_fallback

    @app.post("/api/ai/chat")
    async def chat(request: ChatRequest):
        check_rate_limit(request.user_id)  # your existing rate limiter

        result = chat_with_fallback(
            messages=request.messages,
            max_tokens=1024,
            system_prompt=SYSTEM_PROMPT,  # your existing system prompt
        )

        log_episode(
            user_message    = request.messages[-1]["content"],
            assistant_message = result["content"],
            model_used      = result["model_used"],   # NEW field
            input_tokens    = result["input_tokens"],
            output_tokens   = result["output_tokens"],
            latency_ms      = result["latency_ms"],
            fallback_used   = result["fallback_used"], # NEW field
        )

        return {
            "content":      result["content"],
            "model_used":   result["model_used"],
            "fallback_used": result["fallback_used"],
        }
"""

# ── Standalone test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Fallback Chain — Standalone Test")
    print(f"Chain: {' > '.join(FALLBACK_CHAIN)}\n")

    test_messages = [
        {"role": "user", "content": "In one sentence, what is a fallback chain?"}
    ]

    try:
        result = chat_with_fallback(test_messages, max_tokens=100)
        print(f"Model used:    {result['model_used']}")
        print(f"Fallback used: {result['fallback_used']}")
        print(f"Latency:       {result['latency_ms']}ms")
        print(f"Tokens:        {result['input_tokens']} in / {result['output_tokens']} out")
        print(f"\nResponse:\n{result['content']}")
    except RuntimeError as e:
        print(f"ERROR: {e}")

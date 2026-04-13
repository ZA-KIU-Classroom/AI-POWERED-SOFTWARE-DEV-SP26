"""
LLM Service — wraps OpenRouter and Google AI Studio calls.
All calls are logged with token counts and latency.
"""

import os
import time
import csv
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Client — OpenRouter (preferred) or AI Studio direct fallback
# ---------------------------------------------------------------------------
# Primary: OpenRouter gives access to all models through one key.
# Fallback: If OPENROUTER_KEY is missing, set USE_DIRECT_GEMINI=true
#           and use your personal GEMINI_API_KEY from Google AI Studio.

USE_DIRECT_GEMINI = os.environ.get("USE_DIRECT_GEMINI", "false").lower() == "true"

if USE_DIRECT_GEMINI:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    _openai_client = None
else:
    _openai_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_KEY"],
    )

# ---------------------------------------------------------------------------
# Default model
# ---------------------------------------------------------------------------
# Free tier strategy (April 2026):
#
# Option A — Google AI Studio direct (GEMINI_API_KEY):
#   "gemini-2.5-flash-lite"  → 15 RPM / 1,000 RPD  (fastest, best for prototyping)
#   "gemini-2.5-flash"       → 10 RPM / 250 RPD
#   "gemini-2.5-pro"         → 5 RPM  / 100 RPD
#
# Option B — OpenRouter :free models (no org credits used):
#   "meta-llama/llama-4-maverick:free"  → 20 RPM / 200 RPD
#   "google/gemma-3-27b-it:free"        → 20 RPM / 200 RPD
#   "deepseek/deepseek-r1:free"         → 20 RPM / 200 RPD
#   "openrouter/free"                   → auto-selects best free model
#
# Option C — Paid via org OpenRouter credits (only use when free tier quality
#            is insufficient for your use case):
#   "google/gemini-2.5-flash"           → $0.15 / $0.60 per 1M tokens
#   "google/gemini-2.5-pro"             → $1.25 / $10.00 per 1M tokens
#   "anthropic/claude-haiku-4-5-20251001" → $1.00 / $5.00 per 1M tokens
#
# DEPRECATED — do not use:
#   "gemini-2.0-flash"      → shuts down June 1, 2026
#   "gemini-2.0-flash-lite" → shuts down June 1, 2026

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "google/gemini-2.5-flash")

# ---------------------------------------------------------------------------
# Cost log
# ---------------------------------------------------------------------------
LOG_FILE = os.environ.get("COST_LOG_PATH", "logs/cost-log.csv")

MODEL_PRICING = {
    # Free tier — AI Studio direct
    "gemini-2.5-flash-lite":     {"input": 0.00,  "output": 0.00},
    "gemini-2.5-flash":          {"input": 0.00,  "output": 0.00},
    "gemini-2.5-pro":            {"input": 0.00,  "output": 0.00},
    # Free tier — OpenRouter :free
    "meta-llama/llama-4-maverick:free": {"input": 0.00, "output": 0.00},
    "google/gemma-3-27b-it:free":       {"input": 0.00, "output": 0.00},
    "deepseek/deepseek-r1:free":        {"input": 0.00, "output": 0.00},
    "openrouter/free":                  {"input": 0.00, "output": 0.00},
    # Paid — OpenRouter org credits
    "google/gemini-2.5-flash":          {"input": 0.15,  "output": 0.60},
    "google/gemini-2.5-pro":            {"input": 1.25,  "output": 10.00},
    "anthropic/claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "anthropic/claude-sonnet-4-6":      {"input": 3.00,  "output": 15.00},
    "openai/gpt-4o":                    {"input": 2.50,  "output": 10.00},
}


@dataclass
class CallRecord:
    timestamp:     str
    model:         str
    purpose:       str
    input_tokens:  int
    output_tokens: int
    total_tokens:  int
    latency_ms:    int
    cost_usd:      float


def _log(record: CallRecord) -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=asdict(record).keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(asdict(record))
    print(
        f"[COST] {record.timestamp} | {record.model} | {record.purpose} | "
        f"in={record.input_tokens} out={record.output_tokens} | "
        f"{record.latency_ms}ms | ${record.cost_usd:.6f}"
    )


def _calculate_cost(model: str, in_tok: int, out_tok: int) -> float:
    p = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return (in_tok / 1_000_000) * p["input"] + (out_tok / 1_000_000) * p["output"]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate(
    prompt:  str,
    system:  str = "You are a helpful assistant.",
    model:   str | None = None,
    purpose: str = "generate",
) -> dict:
    """
    Call an AI model and return content + usage metadata.
    Logs every call to logs/cost-log.csv.
    """
    model = model or DEFAULT_MODEL
    start = time.time()

    if USE_DIRECT_GEMINI:
        # Google AI Studio path (free tier fallback)
        import google.generativeai as genai as _genai
        _model    = _genai.GenerativeModel(model, system_instruction=system)
        _response = _model.generate_content(prompt)
        latency   = int((time.time() - start) * 1000)
        meta      = _response.usage_metadata
        in_tok    = meta.prompt_token_count     if meta else 0
        out_tok   = meta.candidates_token_count if meta else 0
        content   = _response.text
    else:
        # OpenRouter path (preferred)
        response  = _openai_client.chat.completions.create(
            model    = model,
            messages = [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
        )
        latency = int((time.time() - start) * 1000)
        usage   = response.usage
        in_tok  = usage.prompt_tokens     if usage else 0
        out_tok = usage.completion_tokens if usage else 0
        content = response.choices[0].message.content

    record = CallRecord(
        timestamp     = datetime.now(timezone.utc).isoformat(),
        model         = model,
        purpose       = purpose,
        input_tokens  = in_tok,
        output_tokens = out_tok,
        total_tokens  = in_tok + out_tok,
        latency_ms    = latency,
        cost_usd      = _calculate_cost(model, in_tok, out_tok),
    )
    _log(record)

    return {
        "content":       content,
        "model":         model,
        "input_tokens":  in_tok,
        "output_tokens": out_tok,
        "latency_ms":    latency,
        "cost_usd":      record.cost_usd,
    }

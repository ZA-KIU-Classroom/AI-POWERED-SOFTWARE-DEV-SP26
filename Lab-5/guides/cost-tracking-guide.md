# Cost Tracking Guide

**CS-AI-2025 Lab 5, Spring 2026**

Every API call your prototype makes must be logged. This is not optional. The data you collect today feeds directly into your Week 11 Safety and Evaluation Audit, which is worth 5 points.

---

## What to Log Per Call

| Field | Type | Example |
|---|---|---|
| timestamp | ISO 8601 string | `2026-04-10T09:23:41Z` |
| model | string | `gemini-2.5-flash` |
| purpose | string | `summarise_document` |
| input_tokens | int | `847` |
| output_tokens | int | `132` |
| total_tokens | int | `979` |
| latency_ms | int | `1240` |
| cost_usd | float | `0.000000` |

---

## Python Implementation (FastAPI)

Create `services/cost_logger.py`:

```python
import csv
import os
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

# Pricing per 1M tokens — verified April 2026
# Free-tier models cost $0.00. Log them anyway so the audit table is complete.
MODEL_PRICING = {
    # --- FREE TIER (Google AI Studio direct) ---
    "gemini-2.5-flash-lite":     {"input": 0.00,  "output": 0.00},
    "gemini-2.5-flash":          {"input": 0.00,  "output": 0.00},
    "gemini-2.5-pro":            {"input": 0.00,  "output": 0.00},
    # --- FREE TIER (OpenRouter :free variants — 20 RPM / 200 RPD) ---
    "meta-llama/llama-4-maverick:free": {"input": 0.00, "output": 0.00},
    "google/gemma-3-27b-it:free":       {"input": 0.00, "output": 0.00},
    "deepseek/deepseek-r1:free":        {"input": 0.00, "output": 0.00},
    # --- PAID via OpenRouter org credits ---
    "google/gemini-2.5-flash":          {"input": 0.15,  "output": 0.60},
    "google/gemini-2.5-pro":            {"input": 1.25,  "output": 10.00},
    "anthropic/claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "anthropic/claude-sonnet-4-6":      {"input": 3.00,  "output": 15.00},
    "openai/gpt-4o":                    {"input": 2.50,  "output": 10.00},
}

LOG_FILE = os.environ.get("COST_LOG_PATH", "logs/cost-log.csv")


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


def _calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return (
        (input_tokens  / 1_000_000) * pricing["input"] +
        (output_tokens / 1_000_000) * pricing["output"]
    )


def log_call(
    model:         str,
    purpose:       str,
    input_tokens:  int,
    output_tokens: int,
    latency_ms:    int,
) -> CallRecord:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    record = CallRecord(
        timestamp     = datetime.now(timezone.utc).isoformat(),
        model         = model,
        purpose       = purpose,
        input_tokens  = input_tokens,
        output_tokens = output_tokens,
        total_tokens  = input_tokens + output_tokens,
        latency_ms    = latency_ms,
        cost_usd      = _calculate_cost(model, input_tokens, output_tokens),
    )

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
    return record
```

Use it in your LLM service:

```python
import time
from services.cost_logger import log_call

def call_model(prompt: str, system: str, model: str, purpose: str) -> dict:
    start = time.time()

    response = client.chat.completions.create(
        model    = model,
        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )

    latency_ms = int((time.time() - start) * 1000)
    usage      = response.usage

    log_call(
        model         = model,
        purpose       = purpose,
        input_tokens  = usage.prompt_tokens     if usage else 0,
        output_tokens = usage.completion_tokens if usage else 0,
        latency_ms    = latency_ms,
    )

    return {
        "content":       response.choices[0].message.content,
        "input_tokens":  usage.prompt_tokens     if usage else 0,
        "output_tokens": usage.completion_tokens if usage else 0,
        "latency_ms":    latency_ms,
    }
```

---

## TypeScript Implementation (Next.js)

Create `lib/cost-logger.ts`:

```typescript
import fs   from "fs";
import path from "path";

const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  // Free tier (Google AI Studio direct)
  "gemini-2.5-flash-lite":      { input: 0.00, output: 0.00 },
  "gemini-2.5-flash":           { input: 0.00, output: 0.00 },
  "gemini-2.5-pro":             { input: 0.00, output: 0.00 },
  // Free tier (OpenRouter :free variants)
  "meta-llama/llama-4-maverick:free": { input: 0.00, output: 0.00 },
  "google/gemma-3-27b-it:free":       { input: 0.00, output: 0.00 },
  // Paid (org credits via OpenRouter)
  "google/gemini-2.5-flash":    { input: 0.15,  output: 0.60  },
  "google/gemini-2.5-pro":      { input: 1.25,  output: 10.00 },
  "anthropic/claude-haiku-4-5-20251001": { input: 1.00, output: 5.00 },
  "anthropic/claude-sonnet-4-6":  { input: 3.00, output: 15.00 },
  "openai/gpt-4o":              { input: 2.50,  output: 10.00 },
};

const LOG_FILE = process.env.COST_LOG_PATH ?? "logs/cost-log.csv";

export interface CallRecord {
  timestamp:     string;
  model:         string;
  purpose:       string;
  input_tokens:  number;
  output_tokens: number;
  total_tokens:  number;
  latency_ms:    number;
  cost_usd:      number;
}

function calculateCost(model: string, i: number, o: number): number {
  const p = MODEL_PRICING[model] ?? { input: 0, output: 0 };
  return (i / 1_000_000) * p.input + (o / 1_000_000) * p.output;
}

export function logCall(params: {
  model:        string;
  purpose:      string;
  inputTokens:  number;
  outputTokens: number;
  latencyMs:    number;
}): CallRecord {
  const record: CallRecord = {
    timestamp:     new Date().toISOString(),
    model:         params.model,
    purpose:       params.purpose,
    input_tokens:  params.inputTokens,
    output_tokens: params.outputTokens,
    total_tokens:  params.inputTokens + params.outputTokens,
    latency_ms:    params.latencyMs,
    cost_usd:      calculateCost(params.model, params.inputTokens, params.outputTokens),
  };

  const dir = path.dirname(LOG_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const headers   = Object.keys(record).join(",");
  const values    = Object.values(record).join(",");
  const addHeader = !fs.existsSync(LOG_FILE);
  fs.appendFileSync(LOG_FILE, (addHeader ? headers + "\n" : "") + values + "\n");

  console.log(
    `[COST] ${record.timestamp} | ${record.model} | ${record.purpose} | ` +
    `in=${record.input_tokens} out=${record.output_tokens} | ` +
    `${record.latency_ms}ms | $${record.cost_usd.toFixed(6)}`
  );
  return record;
}
```

---

## Model Pricing Reference (April 2026)

> **Prices change frequently. Always verify at [openrouter.ai/models](https://openrouter.ai/models) or [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing) before your Week 11 audit.**

| Model | Access | Input / 1M | Output / 1M | Free rate limit |
|-------|--------|-----------|-------------|-----------------|
| `gemini-2.5-flash-lite` via AI Studio | Free | $0.00 | $0.00 | 15 RPM / 1,000 RPD |
| `gemini-2.5-flash` via AI Studio | Free | $0.00 | $0.00 | 10 RPM / 250 RPD |
| `gemini-2.5-pro` via AI Studio | Free | $0.00 | $0.00 | 5 RPM / 100 RPD |
| `meta-llama/llama-4-maverick:free` via OpenRouter | Free | $0.00 | $0.00 | 20 RPM / 200 RPD |
| `google/gemma-3-27b-it:free` via OpenRouter | Free | $0.00 | $0.00 | 20 RPM / 200 RPD |
| `deepseek/deepseek-r1:free` via OpenRouter | Free | $0.00 | $0.00 | 20 RPM / 200 RPD |
| `google/gemini-2.5-flash` via OpenRouter | Paid (org credits) | $0.15 | $0.60 | — |
| `google/gemini-2.5-pro` via OpenRouter | Paid (org credits) | $1.25 | $10.00 | — |
| `anthropic/claude-haiku-4-5-20251001` | Paid (org credits) | $1.00 | $5.00 | — |
| `anthropic/claude-sonnet-4-6` | Paid (org credits) | $3.00 | $15.00 | — |
| `openai/gpt-4o` | Paid (org credits) | $2.50 | $10.00 | — |

**Deprecated — do not use:** `gemini-2.0-flash`, `gemini-2.0-flash-lite` — both shut down June 1, 2026.

---

*Cost tracking guide for CS-AI-2025 Lab 5, Spring 2026.*

# Cost Log — Lab 5 Sprint

**Team Name:**
**Date:** 10 April 2026

> Fill this in live during the sprint. One row per API call. Do not reconstruct it after the fact — the data will not be accurate and this log feeds your Week 11 Safety and Evaluation Audit.

---

## Log Table

| # | Timestamp | Model | Endpoint / Purpose | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Input Price/1M | Output Price/1M | Cost (USD) |
|---|-----------|-------|--------------------|-------------|--------------|-------------|-------------|---------------|----------------|------------|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |
| 6 | | | | | | | | | | |
| 7 | | | | | | | | | | |
| 8 | | | | | | | | | | |
| 9 | | | | | | | | | | |
| 10 | | | | | | | | | | |

*(Add more rows as needed)*

---

## Reference Pricing (April 2026)

| Model | Input Price per 1M tokens | Output Price per 1M tokens |
|-------|--------------------------|---------------------------|
| google/gemini-2.0-flash-001 | $0.10 | $0.40 |
| google/gemini-2.5-pro | $1.25 | $10.00 |
| anthropic/claude-sonnet-4-6 | $3.00 | $15.00 |
| openai/gpt-4o | $2.50 | $10.00 |

Check current pricing at [openrouter.ai/models](https://openrouter.ai/models) — prices change.

---

## Cost Formula

```
cost = (input_tokens / 1_000_000) * input_price
     + (output_tokens / 1_000_000) * output_price
```

---

## How to Capture This Programmatically

**Python / OpenAI SDK:**

```python
import time
from datetime import datetime

def log_call(response, purpose: str, model: str):
    usage = response.usage
    latency_ms = ...  # capture with time.time() before/after the call
    
    input_price_per_m  = 0.10   # update for your model
    output_price_per_m = 0.40

    cost = (
        (usage.prompt_tokens     / 1_000_000) * input_price_per_m +
        (usage.completion_tokens / 1_000_000) * output_price_per_m
    )

    print(
        f"{datetime.now().isoformat()} | {model} | {purpose} | "
        f"in={usage.prompt_tokens} out={usage.completion_tokens} | "
        f"latency={latency_ms}ms | cost=${cost:.6f}"
    )
```

**TypeScript:**

```typescript
function logCall(
  usage: { prompt_tokens: number; completion_tokens: number },
  purpose: string,
  model: string,
  latencyMs: number
) {
  const inputPricePerM  = 0.10;
  const outputPricePerM = 0.40;

  const cost =
    (usage.prompt_tokens     / 1_000_000) * inputPricePerM +
    (usage.completion_tokens / 1_000_000) * outputPricePerM;

  console.log(
    `${new Date().toISOString()} | ${model} | ${purpose} | ` +
    `in=${usage.prompt_tokens} out=${usage.completion_tokens} | ` +
    `latency=${latencyMs}ms | cost=$${cost.toFixed(6)}`
  );
}
```

---

## Sprint Summary (fill in at end of lab)

**Total calls made:**
**Total input tokens:**
**Total output tokens:**
**Total cost (USD):**
**Highest-cost single call:**
**Lowest-latency call:**

---

*Save this file to `logs/cost-log.md` in your team repo. Push with your `lab5-checkpoint` tag.*

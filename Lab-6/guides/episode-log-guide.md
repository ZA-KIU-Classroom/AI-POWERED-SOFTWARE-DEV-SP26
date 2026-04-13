# Episode Log Guide

**CS-AI-2025 Lab 6, Spring 2026**

Your episode log is the single most important data artefact for the Week 11 Safety and Evaluation Audit. Lab 5 introduced cost logging for blocking calls. Lab 6 extends it to capture streaming events and tool calls.

---

## What an Episode Is

An episode is any event that the agent perceives, decides, or executes. Every row in your episode log is one of:

| Event type | When it fires |
|---|---|
| `user_message` | A user message is received by the backend |
| `stream_start` | The first token of a streaming response arrives from the model |
| `stream_end` | The `[DONE]` sentinel is received and the stream is closed |
| `tool_call` | The model invokes a function or MCP tool |
| `tool_result` | The result of a tool call is returned to the model |
| `agent_response` | The final text delivered to the user is saved to session history |
| `error` | Any exception or model error during the loop |

---

## Episode Log Schema

Each episode row contains:

| Field | Type | Example |
|---|---|---|
| `episode_id` | string (UUID) | `"ep_9f3a..."` |
| `session_id` | string | `"sess_abc123"` |
| `ts` | ISO 8601 string | `"2026-04-17T09:23:41.123Z"` |
| `event_type` | string | `"tool_call"` |
| `model` | string or null | `"google/gemini-2.5-flash"` |
| `tool_name` | string or null | `"search_knowledge_base"` |
| `arguments` | JSON string or null | `'{"query": "menu", "top_k": 5}'` |
| `result_summary` | string or null | First 200 chars of result |
| `input_tokens` | int or null | `847` |
| `output_tokens` | int or null | `132` |
| `stream_start_ms` | int or null | `1713341021000` |
| `stream_end_ms` | int or null | `1713341023400` |
| `latency_ms` | int | `1240` |
| `was_cancelled` | bool | `false` |
| `success` | bool | `true` |
| `cost_usd` | float | `0.000124` |

---

## Python Implementation

```python
# services/episode_logger.py
import csv
import json
import os
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any

LOG_FILE = os.environ.get("EPISODE_LOG_PATH", "logs/episode-log.csv")

MODEL_PRICING = {
    "google/gemini-2.5-flash":          {"input": 0.15,  "output": 0.60},
    "google/gemini-2.5-pro":            {"input": 1.25,  "output": 10.00},
    "anthropic/claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "anthropic/claude-sonnet-4-6":      {"input": 3.00,  "output": 15.00},
    # Free tier — still log for audit completeness
    "google/gemini-2.5-flash-lite":     {"input": 0.00,  "output": 0.00},
    "meta-llama/llama-4-maverick:free": {"input": 0.00,  "output": 0.00},
}


@dataclass
class Episode:
    session_id:       str
    event_type:       str
    episode_id:       str   = field(default_factory=lambda: f"ep_{uuid.uuid4().hex[:12]}")
    ts:               str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    model:            str | None = None
    tool_name:        str | None = None
    arguments:        str | None = None   # JSON string
    result_summary:   str | None = None
    input_tokens:     int  = 0
    output_tokens:    int  = 0
    stream_start_ms:  int | None = None
    stream_end_ms:    int | None = None
    latency_ms:       int  = 0
    was_cancelled:    bool = False
    success:          bool = True
    cost_usd:         float = 0.0


def _calculate_cost(model: str, in_tok: int, out_tok: int) -> float:
    p = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return (in_tok / 1_000_000) * p["input"] + (out_tok / 1_000_000) * p["output"]


def log_episode(ep: Episode) -> Episode:
    """Write an episode to the CSV log and print a summary to stdout."""
    ep.cost_usd = _calculate_cost(ep.model or "", ep.input_tokens, ep.output_tokens)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    row       = asdict(ep)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(
        f"[EPISODE] {ep.ts[:19]} | {ep.event_type:<15} | "
        f"{ep.tool_name or ep.model or '-':<30} | "
        f"in={ep.input_tokens} out={ep.output_tokens} | "
        f"{ep.latency_ms}ms | ${ep.cost_usd:.6f}"
    )
    return ep


# ─── Convenience helpers ─────────────────────────────────────────────────────

def log_user_message(session_id: str) -> Episode:
    return log_episode(Episode(session_id=session_id, event_type="user_message"))


def log_stream_end(
    session_id: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    stream_start_ms: int,
    stream_end_ms: int,
    was_cancelled: bool = False,
) -> Episode:
    return log_episode(Episode(
        session_id      = session_id,
        event_type      = "stream_end",
        model           = model,
        input_tokens    = input_tokens,
        output_tokens   = output_tokens,
        stream_start_ms = stream_start_ms,
        stream_end_ms   = stream_end_ms,
        latency_ms      = stream_end_ms - stream_start_ms,
        was_cancelled   = was_cancelled,
    ))


def log_tool_call(
    session_id: str,
    tool_name: str,
    arguments: dict,
    result: Any,
    latency_ms: int,
    success: bool = True,
) -> Episode:
    result_str = str(result)
    return log_episode(Episode(
        session_id     = session_id,
        event_type     = "tool_call",
        tool_name      = tool_name,
        arguments      = json.dumps(arguments),
        result_summary = result_str[:200] if result_str else None,
        latency_ms     = latency_ms,
        success        = success,
    ))


def log_error(session_id: str, error: Exception, context: str = "") -> Episode:
    return log_episode(Episode(
        session_id     = session_id,
        event_type     = "error",
        result_summary = f"{context}: {str(error)[:200]}",
        success        = False,
    ))
```

---

## TypeScript Implementation

```typescript
// lib/episode-logger.ts
import fs   from "fs";
import path from "path";

const LOG_FILE = process.env.EPISODE_LOG_PATH ?? "logs/episode-log.csv";

const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  "google/gemini-2.5-flash":           { input: 0.15,  output: 0.60  },
  "google/gemini-2.5-pro":             { input: 1.25,  output: 10.00 },
  "anthropic/claude-haiku-4-5-20251001": { input: 1.00, output: 5.00 },
  "anthropic/claude-sonnet-4-6":       { input: 3.00,  output: 15.00 },
  "meta-llama/llama-4-maverick:free":  { input: 0.00,  output: 0.00  },
};

export interface Episode {
  episode_id:       string;
  session_id:       string;
  ts:               string;
  event_type:       string;
  model?:           string;
  tool_name?:       string;
  arguments?:       string;
  result_summary?:  string;
  input_tokens:     number;
  output_tokens:    number;
  stream_start_ms?: number;
  stream_end_ms?:   number;
  latency_ms:       number;
  was_cancelled:    boolean;
  success:          boolean;
  cost_usd:         number;
}

function calculateCost(model: string, i: number, o: number): number {
  const p = MODEL_PRICING[model] ?? { input: 0, output: 0 };
  return (i / 1_000_000) * p.input + (o / 1_000_000) * p.output;
}

function generateId(): string {
  return `ep_${Math.random().toString(36).slice(2, 14)}`;
}

export function logEpisode(ep: Partial<Episode> & { session_id: string; event_type: string }): Episode {
  const full: Episode = {
    episode_id:   ep.episode_id   ?? generateId(),
    session_id:   ep.session_id,
    ts:           ep.ts           ?? new Date().toISOString(),
    event_type:   ep.event_type,
    model:        ep.model,
    tool_name:    ep.tool_name,
    arguments:    ep.arguments,
    result_summary: ep.result_summary,
    input_tokens:  ep.input_tokens  ?? 0,
    output_tokens: ep.output_tokens ?? 0,
    stream_start_ms: ep.stream_start_ms,
    stream_end_ms:   ep.stream_end_ms,
    latency_ms:    ep.latency_ms    ?? 0,
    was_cancelled: ep.was_cancelled ?? false,
    success:       ep.success       ?? true,
    cost_usd:      calculateCost(ep.model ?? "", ep.input_tokens ?? 0, ep.output_tokens ?? 0),
  };

  if (process.env.NODE_ENV !== "production") {
    try {
      const dir = path.dirname(LOG_FILE);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      const row       = Object.values(full).join(",");
      const addHeader = !fs.existsSync(LOG_FILE);
      const headers   = Object.keys(full).join(",");
      fs.appendFileSync(LOG_FILE, (addHeader ? headers + "\n" : "") + row + "\n");
    } catch { /* read-only FS in production — skip */ }
  }

  console.log(
    `[EPISODE] ${full.ts.slice(0,19)} | ${full.event_type.padEnd(15)} | ` +
    `${(full.tool_name ?? full.model ?? "-").slice(0,30).padEnd(30)} | ` +
    `in=${full.input_tokens} out=${full.output_tokens} | ` +
    `${full.latency_ms}ms | $${full.cost_usd.toFixed(6)}`
  );

  return full;
}
```

---

## Usage in Your Streaming Route

```python
# In your stream generator — Python example
from services.episode_logger import log_user_message, log_stream_end, log_error
import time

async def handle_stream(session_id: str, messages: list, model: str):
    log_user_message(session_id)
    stream_start = int(time.time() * 1000)

    try:
        # ... your streaming code ...
        # When stream finishes:
        log_stream_end(
            session_id      = session_id,
            model           = model,
            input_tokens    = input_tokens_from_usage,
            output_tokens   = output_tokens_from_usage,
            stream_start_ms = stream_start,
            stream_end_ms   = int(time.time() * 1000),
        )
    except Exception as e:
        log_error(session_id, e, context="stream_generation")
        raise
```

---

## What the Week 11 Audit Expects

Your episode log must cover the period from Lab 6 onwards. The auditor will check:

1. Every tool call has a corresponding episode row with `event_type = "tool_call"`
2. Every streaming call has a row with `stream_start_ms` and `stream_end_ms`
3. Costs are calculated correctly for paid model calls
4. Errors are logged and not silently swallowed
5. No session data from one user appears in another user's rows

Start logging from your first Lab 6 commit. You cannot reconstruct this data retroactively.

---

*Episode log guide for CS-AI-2025 Lab 6, Spring 2026.*

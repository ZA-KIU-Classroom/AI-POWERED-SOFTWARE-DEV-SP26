# Episode Log — Lab 6 Sprint

**Team Name:**
**Date:** 17 April 2026

> The episode log captures every meaningful event your agent produces during a session. Fill it in live — your episode logger should print to the terminal automatically. Copy the terminal output into this table at the end of the sprint, or let the CSV logger build it for you.

---

## Episode Table

| # | Timestamp | Session ID | Event Type | Model / Tool | Input Tokens | Output Tokens | Latency (ms) | Stream Start | Stream End | Cancelled | Success | Cost (USD) |
|---|-----------|------------|------------|-------------|-------------|--------------|-------------|-------------|-----------|-----------|---------|------------|
| 1 | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | |
| 5 | | | | | | | | | | | | |
| 6 | | | | | | | | | | | | |
| 7 | | | | | | | | | | | | |
| 8 | | | | | | | | | | | | |
| 9 | | | | | | | | | | | | |
| 10 | | | | | | | | | | | | |

*(Add rows as needed — aim for at least one row per event type)*

---

## Event Type Reference

| Event type | When it fires |
|---|---|
| `user_message` | A user message arrives at the backend |
| `stream_start` | First token received from model |
| `stream_end` | `[DONE]` sentinel received, full response assembled |
| `tool_call` | Model invokes a function or MCP tool |
| `tool_result` | Result of a tool call returned to the model |
| `agent_response` | Final text saved to session history |
| `error` | Any exception or model error |

---

## Sprint Summary

Fill in at the end of lab.

**Total episodes logged:**
**Total streaming calls:**
**Total tool calls:**
**Total input tokens:**
**Total output tokens:**
**Total cost (USD):**
**Fastest streaming call (latency_ms):**
**Slowest streaming call (latency_ms):**
**Any errors encountered:** Yes / No — describe:

---

## Model Pricing Reference (April 2026)

| Model | Input per 1M tokens | Output per 1M tokens |
|-------|--------------------|--------------------|
| `google/gemini-2.5-flash` (free tier via AI Studio) | $0.00 | $0.00 |
| `google/gemini-2.5-flash` (paid via OpenRouter) | $0.15 | $0.60 |
| `google/gemini-2.5-pro` (paid via OpenRouter) | $1.25 | $10.00 |
| `anthropic/claude-haiku-4-5-20251001` | $1.00 | $5.00 |
| `meta-llama/llama-4-maverick:free` | $0.00 | $0.00 |

Check current prices at [openrouter.ai/models](https://openrouter.ai/models) — prices change.

**Deprecated — do not use:** `gemini-2.0-flash`, `gemini-2.0-flash-lite` (shutdown June 1, 2026).

---

*Save this file to `logs/episode-log-lab6.md` in your team repo. Push with your `lab6-mcp-checkpoint` tag.*

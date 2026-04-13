"""
Episode Logger — CS-AI-2025 Lab 6, Spring 2026

Records every meaningful agent event to a CSV file and stdout.
Extends the Lab 5 cost log to capture streaming calls, tool calls,
and errors in a single unified table.

This log is required for the Week 11 Safety and Evaluation Audit.
Start logging from Lab 6 onwards — you cannot reconstruct this data retroactively.
"""

import csv
import json
import os
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any

LOG_FILE = os.environ.get("EPISODE_LOG_PATH", "logs/episode-log.csv")

# ---------------------------------------------------------------------------
# Pricing — verified April 2026
# Update before the Week 11 Safety and Evaluation Audit.
# Current prices: https://openrouter.ai/models
# ---------------------------------------------------------------------------
MODEL_PRICING: dict[str, dict[str, float]] = {
    # Free tier — Google AI Studio direct
    "gemini-2.5-flash-lite":              {"input": 0.00,  "output": 0.00},
    "gemini-2.5-flash":                   {"input": 0.00,  "output": 0.00},
    "gemini-2.5-pro":                     {"input": 0.00,  "output": 0.00},
    # Free tier — OpenRouter :free models (20 RPM / 200 RPD)
    "meta-llama/llama-4-maverick:free":   {"input": 0.00,  "output": 0.00},
    "google/gemma-3-27b-it:free":         {"input": 0.00,  "output": 0.00},
    "deepseek/deepseek-r1:free":          {"input": 0.00,  "output": 0.00},
    "openrouter/free":                    {"input": 0.00,  "output": 0.00},
    # Paid — OpenRouter org credits
    "google/gemini-2.5-flash":            {"input": 0.15,  "output": 0.60},
    "google/gemini-2.5-pro":             {"input": 1.25,  "output": 10.00},
    "anthropic/claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "anthropic/claude-sonnet-4-6":        {"input": 3.00,  "output": 15.00},
    "openai/gpt-4o":                      {"input": 2.50,  "output": 10.00},
    # DEPRECATED — do not use (shutdown June 1, 2026)
    # "gemini-2.0-flash":  removed
    # "gemini-2.0-flash-lite": removed
}


# ---------------------------------------------------------------------------
# Episode dataclass
# ---------------------------------------------------------------------------

@dataclass
class Episode:
    session_id:       str
    event_type:       str
    # Auto-generated fields
    episode_id:       str   = field(default_factory=lambda: f"ep_{uuid.uuid4().hex[:12]}")
    ts:               str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # Optional fields — populated depending on event type
    model:            str | None   = None
    tool_name:        str | None   = None
    arguments:        str | None   = None   # JSON string
    result_summary:   str | None   = None   # first 200 chars of result
    input_tokens:     int          = 0
    output_tokens:    int          = 0
    stream_start_ms:  int | None   = None
    stream_end_ms:    int | None   = None
    latency_ms:       int          = 0
    was_cancelled:    bool         = False
    success:          bool         = True
    cost_usd:         float        = 0.0


# ---------------------------------------------------------------------------
# Core logging function
# ---------------------------------------------------------------------------

def log_episode(ep: Episode) -> Episode:
    """
    Calculate cost, write to CSV, and print a summary line to stdout.
    Returns the episode with cost_usd populated.
    """
    ep.cost_usd = _calculate_cost(ep.model or "", ep.input_tokens, ep.output_tokens)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    row         = asdict(ep)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    _print_summary(ep)
    return ep


# ---------------------------------------------------------------------------
# Convenience helpers — one per event type
# ---------------------------------------------------------------------------

def log_user_message(session_id: str) -> Episode:
    """Call when a user message is received by the backend."""
    return log_episode(Episode(
        session_id = session_id,
        event_type = "user_message",
    ))


def log_stream_end(
    session_id:      str,
    model:           str,
    input_tokens:    int,
    output_tokens:   int,
    stream_start_ms: int,
    stream_end_ms:   int,
    was_cancelled:   bool = False,
) -> Episode:
    """Call when the streaming response is complete (or cancelled)."""
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
    tool_name:  str,
    arguments:  dict,
    result:     Any,
    latency_ms: int,
    success:    bool = True,
) -> Episode:
    """Call after every function/tool execution."""
    result_str = str(result) if result is not None else ""
    return log_episode(Episode(
        session_id     = session_id,
        event_type     = "tool_call",
        tool_name      = tool_name,
        arguments      = json.dumps(arguments),
        result_summary = result_str[:200] if result_str else None,
        latency_ms     = latency_ms,
        success        = success,
    ))


def log_error(
    session_id: str,
    error:      Exception,
    context:    str = "",
) -> Episode:
    """Call when any exception occurs in the agent loop."""
    return log_episode(Episode(
        session_id     = session_id,
        event_type     = "error",
        result_summary = f"{context}: {str(error)[:190]}" if context else str(error)[:200],
        success        = False,
    ))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
    return (
        (input_tokens  / 1_000_000) * pricing["input"] +
        (output_tokens / 1_000_000) * pricing["output"]
    )


def _print_summary(ep: Episode) -> None:
    label = ep.tool_name or ep.model or "-"
    print(
        f"[EPISODE] {ep.ts[:19]} | {ep.event_type:<15} | "
        f"{label:<30} | "
        f"in={ep.input_tokens} out={ep.output_tokens} | "
        f"{ep.latency_ms}ms | ${ep.cost_usd:.6f}"
    )

/**
 * Episode Logger — CS-AI-2025 Lab 6, Spring 2026
 *
 * Records every meaningful agent event to a CSV file and console.
 * Extends the Lab 5 cost logger to capture streaming events, tool calls, and errors.
 *
 * CSV logging is local-dev only — Vercel's filesystem is read-only.
 * In production, console output is captured by Vercel's Logs dashboard.
 * The Week 11 Safety and Evaluation Audit uses the CSV from local development.
 */

import fs   from "fs";
import path from "path";

// ---------------------------------------------------------------------------
// Pricing — verified April 2026
// Update before the Week 11 Safety and Evaluation Audit.
// Current prices: https://openrouter.ai/models
// ---------------------------------------------------------------------------
const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  // Free tier — Google AI Studio direct
  "gemini-2.5-flash-lite":              { input: 0.00,  output: 0.00  },
  "gemini-2.5-flash":                   { input: 0.00,  output: 0.00  },
  "gemini-2.5-pro":                     { input: 0.00,  output: 0.00  },
  // Free tier — OpenRouter :free models
  "meta-llama/llama-4-maverick:free":   { input: 0.00,  output: 0.00  },
  "google/gemma-3-27b-it:free":         { input: 0.00,  output: 0.00  },
  "openrouter/free":                    { input: 0.00,  output: 0.00  },
  // Paid — OpenRouter org credits
  "google/gemini-2.5-flash":            { input: 0.15,  output: 0.60  },
  "google/gemini-2.5-pro":             { input: 1.25,  output: 10.00 },
  "anthropic/claude-haiku-4-5-20251001": { input: 1.00, output: 5.00  },
  "anthropic/claude-sonnet-4-6":        { input: 3.00,  output: 15.00 },
  "openai/gpt-4o":                      { input: 2.50,  output: 10.00 },
};

const LOG_FILE = process.env.EPISODE_LOG_PATH ?? "logs/episode-log.csv";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// Core logging function
// ---------------------------------------------------------------------------

export function logEpisode(partial: Partial<Episode> & { session_id: string; event_type: string }): Episode {
  const ep: Episode = {
    episode_id:    partial.episode_id    ?? generateId(),
    session_id:    partial.session_id,
    ts:            partial.ts            ?? new Date().toISOString(),
    event_type:    partial.event_type,
    model:         partial.model,
    tool_name:     partial.tool_name,
    arguments:     partial.arguments,
    result_summary: partial.result_summary,
    input_tokens:  partial.input_tokens  ?? 0,
    output_tokens: partial.output_tokens ?? 0,
    stream_start_ms: partial.stream_start_ms,
    stream_end_ms:   partial.stream_end_ms,
    latency_ms:    partial.latency_ms    ?? 0,
    was_cancelled: partial.was_cancelled ?? false,
    success:       partial.success       ?? true,
    cost_usd:      calculateCost(partial.model ?? "", partial.input_tokens ?? 0, partial.output_tokens ?? 0),
  };

  // Always log to console — captured by Vercel Logs in production
  const label = ep.tool_name ?? ep.model ?? "-";
  console.log(
    `[EPISODE] ${ep.ts.slice(0, 19)} | ${ep.event_type.padEnd(15)} | ` +
    `${label.slice(0, 30).padEnd(30)} | ` +
    `in=${ep.input_tokens} out=${ep.output_tokens} | ` +
    `${ep.latency_ms}ms | $${ep.cost_usd.toFixed(6)}`
  );

  // Write to CSV in local development only
  if (process.env.NODE_ENV !== "production") {
    try {
      const dir     = path.dirname(LOG_FILE);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

      const headers   = Object.keys(ep).join(",");
      const values    = Object.values(ep).map(v => (v === undefined || v === null) ? "" : String(v)).join(",");
      const addHeader = !fs.existsSync(LOG_FILE);

      fs.appendFileSync(LOG_FILE, (addHeader ? headers + "\n" : "") + values + "\n");
    } catch {
      // Silently skip on read-only filesystems (Vercel production)
    }
  }

  return ep;
}

// ---------------------------------------------------------------------------
// Convenience helpers — one per event type
// ---------------------------------------------------------------------------

export function logUserMessage(sessionId: string): Episode {
  return logEpisode({ session_id: sessionId, event_type: "user_message" });
}

export function logStreamEnd(params: {
  session_id:      string;
  model:           string;
  input_tokens:    number;
  output_tokens:   number;
  stream_start_ms: number;
  stream_end_ms:   number;
  was_cancelled?:  boolean;
}): Episode {
  return logEpisode({
    session_id:      params.session_id,
    event_type:      "stream_end",
    model:           params.model,
    input_tokens:    params.input_tokens,
    output_tokens:   params.output_tokens,
    stream_start_ms: params.stream_start_ms,
    stream_end_ms:   params.stream_end_ms,
    latency_ms:      params.stream_end_ms - params.stream_start_ms,
    was_cancelled:   params.was_cancelled ?? false,
  });
}

export function logToolCall(params: {
  session_id:  string;
  tool_name:   string;
  arguments:   Record<string, unknown>;
  result:      unknown;
  latency_ms:  number;
  success?:    boolean;
}): Episode {
  const resultStr = params.result !== undefined ? String(params.result) : "";
  return logEpisode({
    session_id:     params.session_id,
    event_type:     "tool_call",
    tool_name:      params.tool_name,
    arguments:      JSON.stringify(params.arguments),
    result_summary: resultStr.slice(0, 200) || undefined,
    latency_ms:     params.latency_ms,
    success:        params.success ?? true,
  });
}

export function logError(sessionId: string, error: Error, context = ""): Episode {
  return logEpisode({
    session_id:     sessionId,
    event_type:     "error",
    result_summary: context ? `${context}: ${error.message.slice(0, 190)}` : error.message.slice(0, 200),
    success:        false,
  });
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

function calculateCost(model: string, inputTokens: number, outputTokens: number): number {
  const p = MODEL_PRICING[model] ?? { input: 0, output: 0 };
  return (inputTokens / 1_000_000) * p.input + (outputTokens / 1_000_000) * p.output;
}

function generateId(): string {
  return `ep_${Math.random().toString(36).slice(2, 14)}`;
}

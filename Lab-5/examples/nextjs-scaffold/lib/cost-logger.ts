/**
 * Cost Logger — records every AI call to logs/cost-log.csv
 * and console. Vercel captures console output in its Logs dashboard.
 * CS-AI-2025 Lab 5, Spring 2026
 */

import fs   from "fs";
import path from "path";

// Pricing per 1M tokens — verified April 2026
// Update before your Week 11 Safety and Evaluation Audit.
// Current prices: https://openrouter.ai/models
const MODEL_PRICING: Record<string, { input: number; output: number }> = {
  // Free tier — OpenRouter :free variants (0 credits charged)
  "google/gemini-2.5-flash":           { input: 0.00,  output: 0.00  }, // free on :free suffix
  "meta-llama/llama-4-maverick:free":  { input: 0.00,  output: 0.00  },
  "google/gemma-3-27b-it:free":        { input: 0.00,  output: 0.00  },
  "openrouter/free":                   { input: 0.00,  output: 0.00  },
  // Paid — OpenRouter org credits
  "google/gemini-2.5-flash-paid":      { input: 0.15,  output: 0.60  },
  "google/gemini-2.5-pro":             { input: 1.25,  output: 10.00 },
  "anthropic/claude-haiku-4-5-20251001": { input: 1.00, output: 5.00 },
  "anthropic/claude-sonnet-4-6":       { input: 3.00,  output: 15.00 },
  "openai/gpt-4o":                     { input: 2.50,  output: 10.00 },
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

function calculateCost(model: string, input: number, output: number): number {
  const p = MODEL_PRICING[model] ?? { input: 0, output: 0 };
  return (input / 1_000_000) * p.input + (output / 1_000_000) * p.output;
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

  // Always log to console — captured by Vercel Logs in production
  console.log(
    `[COST] ${record.timestamp} | ${record.model} | ${record.purpose} | ` +
    `in=${record.input_tokens} out=${record.output_tokens} | ` +
    `${record.latency_ms}ms | $${record.cost_usd.toFixed(6)}`
  );

  // Write to CSV in local development (not available on Vercel's read-only FS)
  if (process.env.NODE_ENV !== "production") {
    try {
      const dir = path.dirname(LOG_FILE);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      const headers   = Object.keys(record).join(",");
      const values    = Object.values(record).join(",");
      const addHeader = !fs.existsSync(LOG_FILE);
      fs.appendFileSync(LOG_FILE, (addHeader ? headers + "\n" : "") + values + "\n");
    } catch {
      // Silently skip on read-only filesystems (Vercel production)
    }
  }

  return record;
}

/**
 * LLM Service — wraps OpenRouter calls for the Next.js scaffold.
 * Every call is logged with tokens and latency.
 * CS-AI-2025 Lab 5, Spring 2026
 */

import OpenAI from "openai";
import { logCall } from "./cost-logger";

// ---------------------------------------------------------------------------
// Client — OpenRouter (preferred)
// ---------------------------------------------------------------------------
// OpenRouter gives access to every model through one key and one credit balance.
// The key is set in .env.local as OPENROUTER_KEY (no NEXT_PUBLIC_ prefix).

const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey:  process.env.OPENROUTER_KEY ?? "",
});

// ---------------------------------------------------------------------------
// Model strategy (April 2026)
// ---------------------------------------------------------------------------
//
// FREE TIER — zero cost, start here:
//
//   OpenRouter :free models (20 RPM / 200 RPD, no credits charged):
//     "google/gemini-2.5-flash"           ← default recommendation
//     "meta-llama/llama-4-maverick:free"
//     "google/gemma-3-27b-it:free"
//     "openrouter/free"                   ← auto-selects best free model
//
// PAID — use org credits only when free quality is insufficient:
//     "google/gemini-2.5-flash"           ← $0.15/$0.60 per 1M tokens
//     "google/gemini-2.5-pro"             ← $1.25/$10.00 per 1M tokens
//     "anthropic/claude-haiku-4-5-20251001" ← $1.00/$5.00 per 1M tokens
//     "anthropic/claude-sonnet-4-6"       ← $3.00/$15.00 per 1M tokens
//
// DEPRECATED — do not use (shutdown June 1, 2026):
//     "google/gemini-2.0-flash"
//     "google/gemini-2.0-flash-lite"

export const DEFAULT_MODEL = process.env.DEFAULT_MODEL ?? "google/gemini-2.5-flash";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ModelCallParams {
  prompt:   string;
  system:   string;
  model?:   string;
  purpose?: string;
}

export interface ModelCallResult {
  content:       string;
  model:         string;
  input_tokens:  number;
  output_tokens: number;
  latency_ms:    number;
  cost_usd:      number;
}

// ---------------------------------------------------------------------------
// callModel
// ---------------------------------------------------------------------------

export async function callModel(params: ModelCallParams): Promise<ModelCallResult> {
  const model   = params.model   ?? DEFAULT_MODEL;
  const purpose = params.purpose ?? "generate";

  const start    = Date.now();
  const response = await client.chat.completions.create({
    model,
    messages: [
      { role: "system", content: params.system },
      { role: "user",   content: params.prompt },
    ],
  });
  const latencyMs = Date.now() - start;

  const usage        = response.usage;
  const inputTokens  = usage?.prompt_tokens     ?? 0;
  const outputTokens = usage?.completion_tokens ?? 0;
  const content      = response.choices[0]?.message?.content ?? "";

  const record = logCall({ model, purpose, inputTokens, outputTokens, latencyMs });

  return {
    content,
    model,
    input_tokens:  inputTokens,
    output_tokens: outputTokens,
    latency_ms:    latencyMs,
    cost_usd:      record.cost_usd,
  };
}

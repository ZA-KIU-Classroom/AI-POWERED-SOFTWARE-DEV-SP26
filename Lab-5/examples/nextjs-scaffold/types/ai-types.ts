/**
 * Shared TypeScript types for AI calls.
 * CS-AI-2025 Lab 5, Spring 2026
 */

// ---------------------------------------------------------------------------
// Request / Response shapes for POST /api/ai
// ---------------------------------------------------------------------------

export interface GenerateRequest {
  prompt:   string;
  system?:  string;
  model?:   string;
}

export interface GenerateResponse {
  content:       string;
  model:         string;
  input_tokens:  number;
  output_tokens: number;
  latency_ms:    number;
  cost_usd:      number;
}

export interface ErrorResponse {
  error:   string;
  detail?: string;
}

// ---------------------------------------------------------------------------
// Cost log record (mirrors cost-logger.ts CallRecord)
// ---------------------------------------------------------------------------

export interface CostLogRecord {
  timestamp:     string;
  model:         string;
  purpose:       string;
  input_tokens:  number;
  output_tokens: number;
  total_tokens:  number;
  latency_ms:    number;
  cost_usd:      number;
}

// ---------------------------------------------------------------------------
// Model registry (April 2026)
// ---------------------------------------------------------------------------

export type ModelTier = "free" | "paid";

export interface ModelInfo {
  id:          string;
  name:        string;
  provider:    string;
  tier:        ModelTier;
  input_price: number;   // USD per 1M tokens
  output_price: number;  // USD per 1M tokens
  rateLimit?:  string;   // e.g. "10 RPM / 250 RPD"
  notes?:      string;
}

export const AVAILABLE_MODELS: ModelInfo[] = [
  // --- Free tier (Google AI Studio direct) ---
  {
    id:           "gemini-2.5-flash-lite",
    name:         "Gemini 2.5 Flash-Lite",
    provider:     "Google AI Studio",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "15 RPM / 1,000 RPD",
    notes:        "Fastest free model. Best for prototyping and high-volume tasks.",
  },
  {
    id:           "gemini-2.5-flash",
    name:         "Gemini 2.5 Flash",
    provider:     "Google AI Studio",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "10 RPM / 250 RPD",
    notes:        "Good quality, still free. Recommended default for most capstone tasks.",
  },
  {
    id:           "gemini-2.5-pro",
    name:         "Gemini 2.5 Pro",
    provider:     "Google AI Studio",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "5 RPM / 100 RPD",
    notes:        "Most capable free model. Use sparingly — 100 requests/day limit.",
  },
  // --- Free tier (OpenRouter :free variants) ---
  {
    id:           "meta-llama/llama-4-maverick:free",
    name:         "Llama 4 Maverick",
    provider:     "OpenRouter (free)",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "20 RPM / 200 RPD",
    notes:        "Strong general-purpose free model. Good for reasoning tasks.",
  },
  {
    id:           "google/gemma-3-27b-it:free",
    name:         "Gemma 3 27B",
    provider:     "OpenRouter (free)",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "20 RPM / 200 RPD",
    notes:        "Good instruction-following. Useful if hitting Gemini rate limits.",
  },
  {
    id:           "openrouter/free",
    name:         "OpenRouter Auto (Free)",
    provider:     "OpenRouter (free)",
    tier:         "free",
    input_price:  0.00,
    output_price: 0.00,
    rateLimit:    "20 RPM / 200 RPD",
    notes:        "Auto-selects best available free model for each request.",
  },
  // --- Paid (org credits via OpenRouter) ---
  {
    id:           "google/gemini-2.5-flash",
    name:         "Gemini 2.5 Flash (paid)",
    provider:     "OpenRouter",
    tier:         "paid",
    input_price:  0.15,
    output_price: 0.60,
    notes:        "Use when free tier quality is insufficient. Best cost/quality ratio.",
  },
  {
    id:           "google/gemini-2.5-pro",
    name:         "Gemini 2.5 Pro (paid)",
    provider:     "OpenRouter",
    tier:         "paid",
    input_price:  1.25,
    output_price: 10.00,
    notes:        "Most capable Gemini. Use for complex reasoning or long documents.",
  },
  {
    id:           "anthropic/claude-haiku-4-5-20251001",
    name:         "Claude Haiku 4.5",
    provider:     "OpenRouter",
    tier:         "paid",
    input_price:  1.00,
    output_price: 5.00,
    notes:        "Fast Anthropic model. Good for structured output and classification.",
  },
  {
    id:           "anthropic/claude-sonnet-4-6",
    name:         "Claude Sonnet 4.6",
    provider:     "OpenRouter",
    tier:         "paid",
    input_price:  3.00,
    output_price: 15.00,
    notes:        "High capability. Reserve for complex generation tasks.",
  },
];

// Convenience: get all free models
export const FREE_MODELS = AVAILABLE_MODELS.filter((m) => m.tier === "free");

// Convenience: get pricing for a model ID
export function getModelPricing(modelId: string): { input: number; output: number } {
  const found = AVAILABLE_MODELS.find((m) => m.id === modelId);
  return found
    ? { input: found.input_price, output: found.output_price }
    : { input: 0, output: 0 };
}

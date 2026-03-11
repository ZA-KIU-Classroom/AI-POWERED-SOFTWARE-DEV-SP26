"""
CS-AI-2025 | Lab 1 | Exercise 3 — Token and Cost Tracker
Spring 2026 | Kutaisi International University

This script demonstrates:
  - How to count tokens before making a call (pre-flight check)
  - How to read token usage from responses
  - How to measure latency accurately
  - How to calculate cost across multiple calls
  - How to log results in a structured format

After completing this exercise, you will understand exactly what your
API calls cost — and why cost discipline matters in production AI systems.
"""

import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
except ImportError:
    print("ERROR: google-genai package not installed. Run: pip install google-genai")
    exit(1)


# ─── Configuration ─────────────────────────────────────────────────────────────

MODEL = "gemini-3-flash-preview"

# Pricing reference (gemini-3-flash-preview paid tier) — for calculation awareness
# You are on the free tier, so actual cost is $0.00
PRICE_INPUT_PER_MILLION  = 0.10   # USD
PRICE_OUTPUT_PER_MILLION = 0.40   # USD

# Test prompts of varying sizes to see how token count affects cost
TEST_PROMPTS = [
    {
        "label": "Tiny prompt",
        "text": "What is Python?"
    },
    {
        "label": "Short prompt",
        "text": "Explain the difference between a list and a tuple in Python, with one example of when you would choose each."
    },
    {
        "label": "Medium prompt",
        "text": """You are reviewing a Python function for a production AI application. 
The function calls an LLM API, processes the response, and stores results in a database.
Identify the three most critical issues with this code and explain how to fix each one:

def process_user_query(query, user_id):
    api_key = "sk-abc123hardcoded"
    import requests
    response = requests.post("https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "gpt-4", "messages": [{"role": "user", "content": query}]}
    )
    result = response.json()["choices"][0]["message"]["content"]
    db.execute(f"INSERT INTO logs VALUES ('{user_id}', '{result}')")
    return result"""
    },
    {
        "label": "Large prompt (few-shot with context)",
        "text": """You are a senior technical writer. Convert the following API documentation
into beginner-friendly tutorial prose. Maintain accuracy but replace all jargon with
plain language. Add a brief "why this matters" for each concept.

ORIGINAL DOCUMENTATION:
Tokenization is the process of converting raw text into a sequence of tokens, where each
token represents a semantically meaningful unit. The tokenizer employed by most modern
LLMs uses Byte-Pair Encoding (BPE), a subword tokenization algorithm that iteratively
merges the most frequent character pairs in the training corpus until a target vocabulary
size is reached. The resulting vocabulary typically contains complete words for high-frequency
items and subword units for rare or compound words. This design balances vocabulary size
(typically 32,000–100,000 tokens) with the model's ability to handle out-of-vocabulary terms
by decomposing them into known subword pieces. Inference costs scale linearly with token count
across both the prompt (input tokens) and completion (output tokens), with providers typically
charging separately for each at different per-token rates due to the differing computational
requirements of the prefill and decode phases of the attention mechanism.

Write the tutorial version now:"""
    }
]


# ─── Cost Calculation ──────────────────────────────────────────────────────────

def calculate_cost(input_tokens, output_tokens):
    """Returns estimated cost in USD at gemini-3-flash-preview paid tier rates."""
    input_cost  = (input_tokens  / 1_000_000) * PRICE_INPUT_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * PRICE_OUTPUT_PER_MILLION
    return input_cost + output_cost


# ─── Logging ───────────────────────────────────────────────────────────────────

def create_log_entry(label, prompt, response, latency_ms):
    """Creates a structured log entry for one API call."""
    usage = response.usage_metadata
    cost  = calculate_cost(usage.prompt_token_count, usage.candidates_token_count)

    return {
        "timestamp":      datetime.now().isoformat(),
        "label":          label,
        "model":          MODEL,
        "prompt_preview": prompt[:80] + "..." if len(prompt) > 80 else prompt,
        "input_tokens":   usage.prompt_token_count,
        "output_tokens":  usage.candidates_token_count,
        "total_tokens":   usage.total_token_count,
        "latency_ms":     round(latency_ms, 1),
        "cost_free_tier": 0.00,
        "cost_paid_tier_reference": round(cost, 8),
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
        exit(1)

    client = genai.Client(api_key=api_key)

    print(f"\nCS-AI-2025 Lab 1 — Token and Cost Tracker")
    print(f"Model: {MODEL}")
    print(f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nRunning {len(TEST_PROMPTS)} test prompts of varying sizes...")
    print(f"(4 second pause between calls to respect the 15 RPM free tier limit)\n")

    session_log = []

    for i, prompt_config in enumerate(TEST_PROMPTS):
        label  = prompt_config["label"]
        prompt = prompt_config["text"]

        print(f"\n{'─'*60}")
        print(f"TEST {i+1}/{len(TEST_PROMPTS)}: {label}")
        print(f"{'─'*60}")

        # Pre-flight token count (before the actual call)
        pre_count = client.models.count_tokens(model=MODEL, contents=prompt)
        print(f"Pre-flight token estimate: {pre_count.total_tokens} tokens")
        print(f"Sending request...")

        # The actual call
        start      = time.perf_counter()
        response   = client.models.generate_content(model=MODEL, contents=prompt)
        latency_ms = (time.perf_counter() - start) * 1000

        # Log entry
        entry = create_log_entry(label, prompt, response, latency_ms)
        session_log.append(entry)

        # Display
        usage = response.usage_metadata
        cost_ref = calculate_cost(usage.prompt_token_count, usage.candidates_token_count)

        print(f"\nResponse preview: {response.text[:120]}...")
        print(f"\nMetrics:")
        print(f"  Input tokens:             {usage.prompt_token_count:>8}")
        print(f"  Output tokens:            {usage.candidates_token_count:>8}")
        print(f"  Total tokens:             {usage.total_token_count:>8}")
        print(f"  Latency:                  {latency_ms:>7.0f} ms")
        print(f"  Cost (free tier):         {'$0.00':>10}")
        print(f"  Cost (paid tier ref):     ${cost_ref:>10.6f}")

        # Pause between calls (skip after last one)
        if i < len(TEST_PROMPTS) - 1:
            print(f"\n[Waiting 4s before next call...]")
            time.sleep(4)

    # ─── Session Summary ───────────────────────────────────────────────────────

    print(f"\n\n{'='*60}")
    print("SESSION SUMMARY")
    print(f"{'='*60}")
    print(f"\n{'Label':<35} {'Input':>8} {'Output':>8} {'Total':>8} {'ms':>8} {'Cost Ref':>12}")
    print("─" * 85)

    total_input   = 0
    total_output  = 0
    total_tokens  = 0
    total_cost    = 0.0
    total_latency = 0.0

    for entry in session_log:
        print(
            f"{entry['label']:<35} "
            f"{entry['input_tokens']:>8} "
            f"{entry['output_tokens']:>8} "
            f"{entry['total_tokens']:>8} "
            f"{entry['latency_ms']:>7.0f}ms "
            f"  ${entry['cost_paid_tier_reference']:>10.6f}"
        )
        total_input   += entry["input_tokens"]
        total_output  += entry["output_tokens"]
        total_tokens  += entry["total_tokens"]
        total_cost    += entry["cost_paid_tier_reference"]
        total_latency += entry["latency_ms"]

    print("─" * 85)
    print(
        f"{'TOTAL':<35} "
        f"{total_input:>8} "
        f"{total_output:>8} "
        f"{total_tokens:>8} "
        f"{total_latency:>7.0f}ms "
        f"  ${total_cost:>10.6f}"
    )

    print(f"\nActual cost today (free tier): $0.00")
    print(f"Reference cost if paid:        ${total_cost:.6f} ({total_cost*100:.4f} cents)")

    avg_latency = total_latency / len(session_log)
    print(f"Average latency per call:      {avg_latency:.0f} ms")

    # ─── Scale calculation ─────────────────────────────────────────────────────

    print(f"\n{'─'*60}")
    print("SCALE EXERCISE — What if you had real users?")
    print(f"{'─'*60}")

    avg_tokens_per_call = total_tokens / len(session_log)
    avg_cost_per_call   = total_cost   / len(session_log)

    scale_scenarios = [
        ("100 users, 10 calls/user/day",   100  * 10),
        ("1,000 users, 10 calls/user/day", 1000 * 10),
        ("10,000 users, 10 calls/user/day",10000* 10),
    ]

    print(f"\n(Based on average of {avg_tokens_per_call:.0f} tokens per call)")
    print(f"{'Scenario':<40} {'Daily calls':>12} {'Daily cost':>14} {'Monthly':>14}")
    print("─" * 82)
    for label, daily_calls in scale_scenarios:
        daily_cost   = daily_calls * avg_cost_per_call
        monthly_cost = daily_cost * 30
        print(f"{label:<40} {daily_calls:>12,} {daily_cost:>13.2f}  {monthly_cost:>13.2f}")

    # Save the session log to JSON for your records
    log_filename = f"token_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_filename, "w") as f:
        json.dump(session_log, f, indent=2)

    print(f"\nSession log saved to: {log_filename}")
    print("Include this file in your homework submission.")

    print("\n" + "="*60)
    print("REFLECTION QUESTIONS — think about these before Lab ends:")
    print("="*60)
    print("1. Why does output token cost more than input token cost?")
    print("2. Your 'large prompt' used more input tokens. How does this")
    print("   affect cost in a multi-turn conversation?")
    print("3. Which scenario in the scale exercise surprised you most?")
    print("4. What would you do to reduce cost per call for the 10K user scenario?")
    print("\n✓ Exercise 3 complete. You have finished all three lab exercises.")
    print("  Next: Review homework requirements in homework/hw1-individual.md")


if __name__ == "__main__":
    main()

"""
eval/run_model_comparison.py
Lab 11 — Multi-Model Benchmark Script

Runs every question in eval/golden_set.json through a list of models
via OpenRouter and writes results to eval/model-comparison.json.

Usage:
    python eval/run_model_comparison.py

Environment variables (set in .env):
    OPENROUTER_API_KEY  — required
    PRIMARY_MODEL       — included in benchmark automatically
    SECONDARY_MODEL     — included in benchmark automatically
    OSS_FALLBACK        — included in benchmark automatically

Override the model list for a single run:
    BENCHMARK_MODELS="anthropic/claude-sonnet-4-6,google/gemini-3-flash" \\
        python eval/run_model_comparison.py
"""

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ────────────────────────────────────────────────────────────

GOLDEN_SET_PATH       = Path("eval/golden_set.json")
OUTPUT_PATH           = Path("eval/model-comparison.json")
SUMMARY_PATH          = Path("eval/model-comparison-summary.md")

LLM_TIMEOUT_SECONDS   = 30.0
DELAY_BETWEEN_CALLS   = 1.0   # seconds between requests — avoids rate limits
MAX_TOKENS            = 512   # keep responses short for benchmarking

# Model pricing — input / output per 1M tokens (USD)
# Update these if provider pricing changes
MODEL_PRICING = {
    "anthropic/claude-sonnet-4-6": (3.00, 15.00),
    "anthropic/claude-opus-4-6":   (15.00, 75.00),
    "google/gemini-3-pro":         (2.00, 12.00),
    "google/gemini-3-flash":       (0.075, 0.30),
    "openai/gpt-4o":               (2.50, 10.00),
    "openai/o3":                   (10.00, 40.00),
    "qwen/qwen-3.5-32b":           (0.20, 0.60),
    "deepseek/deepseek-v4-flash":  (0.14, 0.28),
    "meta-llama/llama-4-scout":    (0.17, 0.17),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Model list ───────────────────────────────────────────────────────────────

def build_model_list() -> list[str]:
    """
    Build the list of models to benchmark.
    Uses BENCHMARK_MODELS env var if set, otherwise reads PRIMARY_MODEL,
    SECONDARY_MODEL, and OSS_FALLBACK from .env.
    """
    override = os.environ.get("BENCHMARK_MODELS", "")
    if override:
        return [m.strip() for m in override.split(",") if m.strip()]

    models = []
    for key in ("PRIMARY_MODEL", "SECONDARY_MODEL", "OSS_FALLBACK"):
        val = os.environ.get(key, "")
        if val and val not in models:
            models.append(val)

    if not models:
        # Defaults if nothing is configured
        models = [
            "anthropic/claude-sonnet-4-6",
            "google/gemini-3-flash",
            "qwen/qwen-3.5-32b",
        ]

    return models

# ── Golden set ───────────────────────────────────────────────────────────────

def load_golden_set() -> list[dict]:
    """
    Load questions from eval/golden_set.json.
    Supports both formats:
      {"questions": [...]}              — standard format
      [{"id": "q001", "prompt": ...}]   — flat list format
    """
    if not GOLDEN_SET_PATH.exists():
        raise FileNotFoundError(
            f"Golden set not found at {GOLDEN_SET_PATH}. "
            "Create it before running the benchmark."
        )

    with open(GOLDEN_SET_PATH) as f:
        data = json.load(f)

    if isinstance(data, list):
        questions = data
    elif isinstance(data, dict) and "questions" in data:
        questions = data["questions"]
    else:
        raise ValueError(
            f"Unexpected golden set format in {GOLDEN_SET_PATH}. "
            "Expected a list or a dict with a 'questions' key."
        )

    if len(questions) < 5:
        raise ValueError(
            f"Golden set has only {len(questions)} questions. "
            "Add more questions until you have at least 5."
        )

    return questions

# ── Benchmarking ─────────────────────────────────────────────────────────────

def estimate_cost_usd(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Estimate cost in USD based on known pricing table."""
    if model not in MODEL_PRICING:
        return 0.0  # unknown model — cannot estimate
    price_in, price_out = MODEL_PRICING[model]
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


def run_single(
    client: openai.OpenAI,
    model: str,
    question: dict,
) -> dict:
    """
    Run one question through one model.
    Returns a result dict regardless of success or failure.
    """
    prompt = question.get("prompt") or question.get("question") or ""
    q_id   = question.get("id", "unknown")

    result = {
        "model":         model,
        "question_id":   q_id,
        "question":      prompt[:300],
        "answer":        None,
        "latency_ms":    None,
        "input_tokens":  None,
        "output_tokens": None,
        "cost_usd":      None,
        "error":         None,
    }

    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            timeout=LLM_TIMEOUT_SECONDS,
        )
        latency_ms = int((time.perf_counter() - start) * 1000)

        content = response.choices[0].message.content or ""
        if not content.strip():
            result["error"] = "empty_response"
        else:
            result["answer"] = content

        result["latency_ms"]    = latency_ms
        result["input_tokens"]  = response.usage.prompt_tokens
        result["output_tokens"] = response.usage.completion_tokens
        result["cost_usd"]      = estimate_cost_usd(
            model,
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
        )

    except openai.APITimeoutError:
        result["error"]      = "timeout"
        result["latency_ms"] = int(LLM_TIMEOUT_SECONDS * 1000)

    except openai.RateLimitError as e:
        result["error"] = f"rate_limit: {str(e)[:80]}"

    except openai.APIStatusError as e:
        result["error"] = f"api_error_{e.status_code}"

    except Exception as e:
        result["error"] = f"unexpected: {str(e)[:80]}"

    return result


def benchmark_all(
    models: list[str],
    questions: list[dict],
) -> list[dict]:
    """Run every question through every model. Returns flat list of results."""
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to your .env file and restart."
        )

    client = openai.OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    all_results = []
    total = len(models) * len(questions)
    done  = 0

    for model in models:
        print(f"\n[{models.index(model)+1}/{len(models)}] {model}")
        for question in questions:
            done += 1
            q_id = question.get("id", "?")
            print(f"  {q_id} [{done}/{total}]", end="", flush=True)

            result = run_single(client, model, question)

            if result["error"]:
                print(f"  ERROR: {result['error']}")
            else:
                print(f"  latency={result['latency_ms']}ms  tokens={result['output_tokens']}")

            all_results.append(result)

            # Delay between calls to avoid rate limits
            if done < total:
                time.sleep(DELAY_BETWEEN_CALLS)

    return all_results

# ── Summary generation ───────────────────────────────────────────────────────

def build_summary(
    results: list[dict],
    models: list[str],
    run_timestamp: str,
) -> str:
    """Build a human-readable markdown summary of benchmark results."""
    lines = [
        f"## Model Benchmark Summary\n",
        f"**Run:** {run_timestamp}  ",
        f"**Models:** {len(models)}  ",
        f"**Questions:** {len(set(r['question_id'] for r in results))}  \n",
    ]

    for model in models:
        model_results = [r for r in results if r["model"] == model]
        successes     = [r for r in model_results if r["error"] is None]
        errors        = [r for r in model_results if r["error"] is not None]

        latencies  = [r["latency_ms"] for r in successes if r["latency_ms"]]
        in_tokens  = [r["input_tokens"] for r in successes if r["input_tokens"]]
        out_tokens = [r["output_tokens"] for r in successes if r["output_tokens"]]
        costs      = [r["cost_usd"] for r in successes if r["cost_usd"]]

        p50 = sorted(latencies)[len(latencies)//2] if latencies else "n/a"
        p95 = sorted(latencies)[int(len(latencies)*0.95)] if len(latencies) >= 2 else "n/a"

        avg_in  = int(sum(in_tokens)  / len(in_tokens))  if in_tokens  else 0
        avg_out = int(sum(out_tokens) / len(out_tokens)) if out_tokens else 0
        avg_cost = sum(costs) / len(costs) if costs else 0.0

        lines += [
            f"### {model}\n",
            f"- **Answered:** {len(successes)}/{len(model_results)} "
            f"({len(errors)} error{'s' if len(errors) != 1 else ''})",
            f"- **Latency:** p50={p50}ms  p95={p95}ms",
            f"- **Tokens:** avg input={avg_in}  avg output={avg_out}",
            f"- **Cost:** ${avg_cost:.6f} per question "
            f"| ${avg_cost*1000:.4f}/1000 questions",
        ]

        if errors:
            lines.append(f"- **Errors:** " + ", ".join(
                f"{r['question_id']}: {r['error']}" for r in errors
            ))
        lines.append("")

    lines += [
        "---\n",
        "_Generated by eval/run_model_comparison.py_\n",
        "_Raw data in eval/model-comparison.json_\n",
    ]
    return "\n".join(lines)

# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Lab 11 — Multi-Model Benchmark")
    print("=" * 60)

    models    = build_model_list()
    questions = load_golden_set()

    print(f"\nModels to benchmark ({len(models)}):")
    for m in models:
        print(f"  {m}")

    print(f"\nQuestions ({len(questions)}):")
    for q in questions:
        q_id = q.get("id", "?")
        text = (q.get("prompt") or q.get("question") or "")[:60]
        print(f"  {q_id}: {text}...")

    print(f"\nRunning benchmark... (estimated {len(models)*len(questions)*1.5:.0f}s)\n")

    run_ts  = datetime.now(timezone.utc).isoformat()
    results = benchmark_all(models, questions)

    # Write raw results
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_timestamp": run_ts,
        "models":        models,
        "question_count": len(questions),
        "results":       results,
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nResults written to {OUTPUT_PATH}")

    # Write summary
    summary = build_summary(results, models, run_ts)
    with open(SUMMARY_PATH, "w") as f:
        f.write(summary)
    print(f"Summary written to {SUMMARY_PATH}")

    # Print summary to terminal
    print("\n" + "=" * 60)
    print(summary)


if __name__ == "__main__":
    main()

# Lab 11 Quick Start

Get from zero to your first benchmark result in under 10 minutes.

---

## Step 1 — Confirm your .env has the three model variables

Open your `.env` file and add these three lines if they are not already there. Replace the model strings if you want to use different models — the ones below are the recommended defaults.

```bash
# Primary model — your production choice
PRIMARY_MODEL=anthropic/claude-sonnet-4-6

# Secondary fallback — activates when primary returns 4xx or 5xx
SECONDARY_MODEL=google/gemini-3-flash

# OSS fallback — last resort, maximally available
OSS_FALLBACK=qwen/qwen-3.5-32b
```

Add the same keys to `.env.example` with placeholder values so your teammates can see what variables are required without exposing real keys:

```bash
# .env.example
PRIMARY_MODEL=anthropic/claude-sonnet-4-6
SECONDARY_MODEL=google/gemini-3-flash
OSS_FALLBACK=qwen/qwen-3.5-32b
OPENROUTER_API_KEY=your-openrouter-key-here
```

---

## Step 2 — Install the benchmark dependencies

```bash
# If using uv (recommended)
uv pip install openai python-dotenv tenacity

# If using pip + venv
pip install openai python-dotenv tenacity --break-system-packages
```

---

## Step 3 — Copy the benchmark script into your project

Copy `examples/benchmark/run_model_comparison.py` from this lab package into your project's `eval/` directory:

```bash
cp Lab-11/examples/benchmark/run_model_comparison.py eval/
```

---

## Step 4 — Run the benchmark

```bash
cd your-capstone-repo/
python eval/run_model_comparison.py
```

The script reads your golden set from `eval/golden_set.json`, runs each question through your three models, and writes results to `eval/model-comparison.json`.

Expected output:

```
Running benchmark across 3 models...
[1/3] anthropic/claude-sonnet-4-6
  Q1: latency=1240ms tokens=312 ✓
  Q2: latency=980ms  tokens=287 ✓
  ...
[2/3] google/gemini-3-flash
  Q1: latency=420ms  tokens=298 ✓
  ...
[3/3] qwen/qwen-3.5-32b
  Q1: latency=1850ms tokens=341 ✓
  ...
Benchmark complete. Results: eval/model-comparison.json
Summary written: eval/model-comparison-summary.md
```

---

## Step 5 — Add the fallback chain to your backend

Copy `examples/fallback_chain/fallback_chain.py` into your backend directory and integrate it with your existing chat endpoint. Full instructions in `guides/fallback-chain-guide.md`.

---

## Step 6 — Update your README

Copy the model selection table template from `templates/model-selection-table.md` and fill it in with your benchmark results. This takes approximately 20 minutes and is worth multiple points on the Repository Review.

---

## Step 7 — Commit, tag, push

```bash
git add -A
git commit -m "lab11: multi-model portability

- eval/model-comparison.json: 3 models benchmarked across N questions
- backend: chat_with_fallback() with PRIMARY > SECONDARY > OSS chain
- model_used field added to all episode log entries
- README: model selection decisions table
- README: cost analysis updated"

git tag lab11-portability
git push origin main --tags
```

---

## Common Problems

**"No module named openai"**  
Run `uv pip install openai` or `pip install openai --break-system-packages`.

**"OPENROUTER_API_KEY not set"**  
Run `export $(cat .env | xargs)` to load your env file, or use `python-dotenv` in the script (already included in the example).

**"Model returned empty response"**  
Some models occasionally return empty completions. The benchmark script retries once automatically. If it persists, the model may be overloaded — try again in 5 minutes.

**"golden_set.json not found"**  
Your golden set must be at `eval/golden_set.json`. If it is elsewhere, update the `GOLDEN_SET_PATH` variable at the top of `run_model_comparison.py`.

**"Rate limit on OpenRouter"**  
The benchmark sends one request at a time with a 1-second delay between calls. If you still hit rate limits, increase `DELAY_BETWEEN_CALLS` from 1.0 to 2.0 in the script.

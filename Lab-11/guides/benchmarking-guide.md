# Guide: Benchmarking Models Against Your Golden Set

This guide explains how to run the multi-model benchmark, interpret the results, and use them to write your model selection table.

---

## What the Benchmark Does

The benchmark script (`eval/run_model_comparison.py`) takes every question from your golden set and sends it to each model in your comparison list. It records:

- The model's answer
- Latency in milliseconds (wall clock, including network)
- Token counts (input and output)
- Estimated cost in USD
- Any errors (timeouts, rate limits, empty responses)

Results are written to `eval/model-comparison.json` and a human-readable summary to `eval/model-comparison-summary.md`.

---

## Before You Run

**Check your golden set has at least 5 questions:**

```bash
python -c "
import json
with open('eval/golden_set.json') as f:
    gs = json.load(f)
print(f'{len(gs[\"questions\"])} questions found')
for q in gs['questions']:
    print(f'  {q[\"id\"]}: {q[\"prompt\"][:60]}...')
"
```

**Golden set format (your file should match this structure):**

```json
{
  "version": "1.0",
  "questions": [
    {
      "id": "q001",
      "prompt": "Your question here",
      "expected_keywords": ["keyword1", "keyword2"],
      "category": "factual"
    },
    {
      "id": "q002",
      "prompt": "Another question",
      "expected_keywords": ["keyword3"],
      "category": "reasoning"
    }
  ]
}
```

If your golden set uses a different format, update the `load_golden_set()` function in the benchmark script.

---

## Running the Benchmark

```bash
# From your capstone repo root
python eval/run_model_comparison.py

# To run with a specific model list (overrides defaults in script)
BENCHMARK_MODELS="anthropic/claude-sonnet-4-6,google/gemini-3-flash" \
  python eval/run_model_comparison.py

# To run against just one model (for debugging)
BENCHMARK_MODELS="google/gemini-3-flash" \
  python eval/run_model_comparison.py
```

The script runs approximately 1-2 minutes for 3 models × 5 questions. During the lab session, start it running and work on something else while it completes.

---

## Reading the Results

After the run, open `eval/model-comparison-summary.md`:

```
## Benchmark Summary — 2026-05-29 09:45

### anthropic/claude-sonnet-4-6
Questions: 5/5 answered (0 errors)
Latency: p50=1240ms p95=1850ms
Tokens:   avg input=187 avg output=312
Cost:     $0.00149 per question | $1.49/1000 questions
Quality:  See answers in model-comparison.json

### google/gemini-3-flash
Questions: 5/5 answered (0 errors)
Latency: p50=420ms p95=680ms
Tokens:   avg input=192 avg output=287
Cost:     $0.000028 per question | $0.028/1000 questions
Quality:  See answers in model-comparison.json

### qwen/qwen-3.5-32b
Questions: 4/5 answered (1 timeout)
Latency: p50=1850ms p95=4200ms
Tokens:   avg input=189 avg output=341
Cost:     $0.000052 per question | $0.052/1000 questions
Quality:  See answers in model-comparison.json
```

**Key questions to answer from this data:**

1. Which model answered every question successfully? (reliability)
2. Which model was fastest at p50? Which was fastest at p95? (latency)
3. What is the cost ratio between your most expensive and cheapest model? (budget)
4. For the questions you can manually evaluate — which answers were best? (quality)

---

## Manually Scoring Answer Quality

The benchmark script records the raw answers but does not score them automatically — automated quality scoring requires an LLM judge, which you can set up as a follow-on exercise. For Lab 11, manually review 2-3 answers per model.

Open `eval/model-comparison.json` and look at the `answer` field for each model's response to the same question. Ask yourself:

- Does the answer correctly address what was asked?
- Is it the right length — not too short, not padding?
- For questions with expected keywords: are they present?
- For reasoning questions: does the model show its work or just give a conclusion?

Write your qualitative assessment in a comment in your commit message or in your team's pull request description. One paragraph per model is enough.

---

## Adding a Fourth Model (optional — strong evidence)

If you finish the required benchmark early, add a fourth model to see how it compares. Good candidates:

```python
# Add to MODELS list in run_model_comparison.py
"meta-llama/llama-4-scout",     # 10M context, unique for long docs
"openai/o3",                     # warning: expensive and slow — use 1 question only
"deepseek/deepseek-v4-flash",   # fast and cheap, good for code
```

For `openai/o3`, limit to 1 question — it costs approximately $0.08 per question and takes 10-15 seconds.

---

## Writing Your Model Selection Table

Once the benchmark is done, write the table in your README. Template in `templates/model-selection-table.md`.

The table should directly reference your benchmark numbers. Vague reasons like "it is good" or "it is fast" do not pass the rubric. Specific reasons like "p50 latency of 420ms vs 1240ms for Claude makes it the right choice for our real-time chat feature" pass the rubric.

**Example of a weak reason:** "We chose Gemini Flash because it is cheap."

**Example of a strong reason:** "Gemini 3 Flash at $0.028/1000 questions is 53x cheaper than Claude Sonnet for this task type. Our benchmark showed answer quality is equivalent on factual questions (both answered 5/5 correctly). For our classification endpoint that runs on every user message, this cost difference saves approximately $40/month at our projected usage."

---

## Interpreting Errors in the Benchmark

**Timeout (error: "timeout"):**  
The model took longer than 30 seconds. This is a real production signal — if your benchmark shows a model timing out 1 in 5 times, it is not suitable as a primary model. Document it.

**RateLimitError (error: "rate_limit"):**  
You hit OpenRouter's rate limit. The script retries once after 5 seconds. If it still fails, reduce `DELAY_BETWEEN_CALLS` to 2.0 seconds and re-run.

**Empty response (error: "empty_response"):**  
The model returned a 200 but with empty content. Rare but real. The script records it as an error and moves on.

**APIStatusError with 404 (error: "model_not_found"):**  
The model string is wrong or the model is not available on OpenRouter. Check `openrouter.ai/models` for the exact string.

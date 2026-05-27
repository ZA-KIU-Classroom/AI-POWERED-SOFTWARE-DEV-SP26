# Template: Model Selection Decisions Table

Copy this section into your README.md and fill it in with your actual benchmark numbers from `eval/model-comparison.json`. Replace every `[PLACEHOLDER]` with real data.

---

## Model Selection Decisions

*Last updated: [DATE] | Benchmark data: `eval/model-comparison.json`*

| Task | Model | Why | Fallback |
|------|-------|-----|----------|
| [Primary chat / Q&A feature] | [e.g. anthropic/claude-sonnet-4-6] | [Specific reason with data: e.g. "p50 latency 1240ms. Answer quality 5/5 on our golden set. Leads on our domain (document analysis). Cache hit rate 68% reduces effective cost to $0.96/M."] | [e.g. google/gemini-3-flash] |
| [Classification / tagging feature] | [e.g. google/gemini-3-flash] | [e.g. "$0.075/M input vs $3.00/M for Claude — 40x cheaper. Our benchmark shows equivalent accuracy on binary classification tasks (5/5 vs 5/5). p50 latency 420ms makes it suitable for synchronous calls."] | [e.g. qwen/qwen-3.5-32b] |
| [Image analysis / multimodal feature] | [e.g. google/gemini-3-pro] | [e.g. "Native multimodal. 2M context window handles our batch processing job. Not available via Claude Sonnet for this use case."] | [e.g. anthropic/claude-sonnet-4-6] |
| [Evaluation / LLM judge] | [e.g. anthropic/claude-opus-4-6] | [e.g. "Highest rubric-scoring quality. Only used in CI runs, not production requests — latency and cost are acceptable for offline evaluation."] | Not applicable |

### Why We Did Not Use [Model X]

*Fill this in for at least one model you evaluated but did not choose as primary.*

[e.g. "We evaluated openai/o3 for our reasoning tasks. Latency of 8-15 seconds per request is incompatible with our real-time chat requirement. We reserve it for offline evaluation jobs only."]

### Fallback Strategy

| Priority | Model | Trigger Condition |
|----------|-------|-------------------|
| 1 (Primary) | [PRIMARY_MODEL] | Always tried first |
| 2 (Secondary) | [SECONDARY_MODEL] | RateLimitError or APIStatusError from primary |
| 3 (OSS fallback) | [OSS_FALLBACK] | RateLimitError or APIStatusError from secondary |
| 4 (Graceful degradation) | Cached response | All providers exhausted |

*The fallback chain is implemented in `backend/llm_client.py`. Fallback activation was verified during Lab 11 — see commit message for log evidence.*

---

## Cost Analysis

*Based on OpenRouter dashboard data for the week of [DATE].*

| Metric | Value |
|--------|-------|
| Total requests last week | [N] |
| Total tokens consumed | [N input] / [N output] |
| Total spend last week | $[X] |
| Average cost per request | $[X] |
| Projected monthly spend (at current usage) | $[X] |
| Primary model cost per 1000 requests | $[X] |
| Secondary model cost per 1000 requests | $[X] |
| Estimated saving from task-based routing | [X]% vs routing all to primary |

### Cost Breakdown by Model

| Model | Requests | Input Tokens | Output Tokens | Spend |
|-------|----------|--------------|---------------|-------|
| [PRIMARY_MODEL] | [N] | [N] | [N] | $[X] |
| [SECONDARY_MODEL] | [N] | [N] | [N] | $[X] |
| [OSS_FALLBACK] | [N] | [N] | [N] | $[X] |

*Data source: OpenRouter activity dashboard at openrouter.ai/activity*

---

## Notes on Writing Strong Reasons

The grader looks for reasons that reference actual data. Compare these two examples:

**Weak (will not pass the rubric):**  
> "We chose Claude because it gives good answers."

**Strong (passes the rubric):**  
> "Our benchmark shows Claude Sonnet 4.6 answered 5/5 golden set questions correctly with p50 latency of 1240ms. It costs $3.00/M input tokens. For our primary chat feature, which accounts for 60% of API calls and requires high accuracy, the quality justifies the cost. Prompt caching at 68% hit rate reduces effective cost to approximately $0.96/M."

The difference: the strong reason tells the reader what you measured, what you found, and why that finding led to your decision.

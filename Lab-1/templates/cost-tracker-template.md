# Cost Tracker Template

**Weekly API cost and usage tracking for CS-AI-2025**

---

## Instructions

Fill in this tracker for every lab and every homework assignment throughout the semester. Completed cost trackers are a required component of all homework submissions.

The point of tracking costs is not to worry about spending money — especially in the early weeks when you are on the free tier. The point is to build the habit of *knowing* what your code costs to run. In production AI applications, cost is a first-class engineering concern. Engineers who cannot estimate and track API costs are not deployable in AI roles.

---

## Student Information

| Field | Value |
|-------|-------|
| Student Name | |
| Student ID | |
| GitHub username | |
| Semester | Spring 2026 |

---

## Lab 1 — Environment Setup and First Application

**Date:** Friday, 6 March 2026  
**Model used:** `gemini-3-flash-preview` (free tier)

### In-Lab Usage

| Exercise | Calls Made | Input Tokens | Output Tokens | Total Tokens | Latency (avg ms) | Cost (USD) |
|----------|-----------|-------------|--------------|-------------|-----------------|------------|
| Exercise 1: Hello AI | | | | | | $0.00 |
| Exercise 2: Prompt Patterns | | | | | | $0.00 |
| Exercise 3: Token Counter | | | | | | $0.00 |
| **Lab 1 Total** | | | | | | **$0.00** |

*Note: All Lab 1 in-lab work uses the free tier. Cost column shows $0.00 but please fill in the token counts — those matter.*

### Homework 1 Usage

| Session | Date | Calls Made | Input Tokens | Output Tokens | Total Tokens | Cost (USD) |
|---------|------|-----------|-------------|--------------|-------------|------------|
| HW1 development session 1 | | | | | | $0.00 |
| HW1 development session 2 | | | | | | $0.00 |
| HW1 development session 3 | | | | | | $0.00 |
| **HW1 Total** | | | | | | **$0.00** |

### Lab 1 + HW1 Combined Summary

| Metric | Value |
|--------|-------|
| Total API calls | |
| Total input tokens | |
| Total output tokens | |
| Total tokens | |
| Average latency (ms) | |
| Total cost (free tier) | $0.00 |
| Cost if on paid tier (`gemini-3-flash-preview`) | *(calculate: input_tokens × $0.10/M + output_tokens × $0.40/M)* |

**Reflection on cost:**

If your Lab 1 work had been on the paid tier, what would it have cost? Is that surprising?

```
[your answer here]
```

---

## Running Weekly Tracker (to maintain throughout the semester)

Update this section each week as a cumulative record.

| Week | Lab | Model(s) Used | Total Calls | Total Tokens | Actual Cost (USD) | Notes |
|------|-----|-------------|-------------|-------------|-------------------|-------|
| 1 | Lab 1 | gemini-3-flash-preview (free) | | | $0.00 | Free tier |
| 2 | Lab 2 | (OpenRouter credits) | | | | |
| 3 | Lab 3 | | | | | |
| 4 | Lab 4 | | | | | |
| 5 | Lab 5 | | | | | |
| 6 | Lab 6 | | | | | |
| 7 | Lab 7 | | | | | |
| 8 | Lab 8 | | | | | |
| 9 | Midterm | N/A | — | — | — | No lab |
| 10 | Lab 10 | | | | | |
| 11 | Lab 11 | | | | | |
| 12 | Lab 12 | | | | | |
| 13 | Lab 13 | | | | | |
| 14 | Lab 14 | | | | | |
| 15 | Final | | | | | |
| **TOTAL** | | | | | | |

---

## Cost Estimation Reference

Use this table for estimating costs before running experiments:

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Good for |
|-------|-----------------------|------------------------|----------|
| `gemini-3-flash-preview` | $0.10 | $0.40 | High-volume, fast tasks |
| `gemini-3.1-flash` | $0.10 | $0.40 | Balanced performance |
| `gemini-3.1-pro` | $1.25 | $5.00 | Complex reasoning tasks |
| `claude-opus-4-6` | $15.00 | $75.00 | Highest quality needed |
| `gpt-5.2` | $10.00 | $30.00 | OpenAI ecosystem tasks |
| `gpt-4.1-mini` | $0.40 | $1.60 | Efficient OpenAI tasks |

*Prices approximate as of March 2026. Always verify at [openrouter.ai/models](https://openrouter.ai/models).*

### Quick estimation formula

```
Estimated cost = (planned_calls × avg_input_tokens / 1,000,000 × input_price)
               + (planned_calls × avg_output_tokens / 1,000,000 × output_price)
```

**Example:** 50 calls with 200 input and 500 output tokens each, using `gemini-3-flash-preview`:
```
Cost = (50 × 200 / 1,000,000 × $0.10) + (50 × 500 / 1,000,000 × $0.40)
     = $0.00075 + $0.0075
     = $0.00825  (less than one cent)
```

---

*Cost Tracker Template for CS-AI-2025, Spring 2026.*  
*This tracker is required in all homework submissions starting from HW1.*

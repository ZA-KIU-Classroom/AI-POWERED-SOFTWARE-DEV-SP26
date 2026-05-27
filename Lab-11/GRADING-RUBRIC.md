# Lab 11 Grading Rubric

**Total: Participation/Labwork (counts toward the 15-point lab component)**  
**Graded by:** git tag `lab11-portability` contents

---

## Part A — Repository Deliverables (Team, assessed from git tag)

### A1. Model Benchmark Results — `eval/model-comparison.json`

| Score | Criteria |
|-------|----------|
| Full | JSON present, at least 3 models tested, at least 5 questions per model, all required fields present (`model`, `question_id`, `answer`, `latency_ms`, `input_tokens`, `output_tokens`, `error`) |
| Partial | JSON present but fewer than 3 models, or fewer than 5 questions, or missing required fields |
| Zero | File absent or contains only placeholder data |

**Required fields in each result object:**
```json
{
  "model": "anthropic/claude-sonnet-4-6",
  "question_id": "q001",
  "question": "What is ...",
  "answer": "...",
  "latency_ms": 1240,
  "input_tokens": 187,
  "output_tokens": 312,
  "cost_usd": 0.00149,
  "error": null
}
```

---

### A2. Fallback Chain Implementation

| Score | Criteria |
|-------|----------|
| Full | `chat_with_fallback()` function (or equivalent) present in backend code. Catches `RateLimitError` and `APIStatusError` separately. Iterates through at least PRIMARY and SECONDARY models. Returns `model_used` in response. |
| Partial | Fallback implemented but catches only bare `Exception`, or only two models in chain (no OSS fallback), or `model_used` missing from response |
| Zero | No fallback logic present — single model called with no error recovery |

---

### A3. `model_used` in Episode Log

| Score | Criteria |
|-------|----------|
| Full | Every entry in episode log (or API response) contains `model_used` field showing which model answered |
| Partial | Field present in some responses but not all |
| Zero | Field absent |

---

### A4. README — Model Selection Decisions Table

| Score | Criteria |
|-------|----------|
| Full | Table present in README with at minimum: task, model, reason for choice, fallback. At least 2 rows covering different task types. Reasons are substantive (not just "it is good") — reference latency, cost, quality, or benchmark results |
| Partial | Table present but reasons are vague, or only one row, or fallback column is empty |
| Zero | Table absent |

---

### A5. README — Cost Analysis Update

| Score | Criteria |
|-------|----------|
| Full | Actual token counts from the past week's usage documented (from OpenRouter dashboard or episode log). Monthly projection calculated. Shows awareness of cost per task type. |
| Partial | Generic estimate without actual data, or projection method not explained |
| Zero | No cost analysis in README |

---

### A6. Git Tag and Commit Quality

| Score | Criteria |
|-------|----------|
| Full | `lab11-portability` tag exists on remote. Commit message describes what was implemented (not "lab 11 done"). Commit is clean — no accidentally committed `.env`, no binary files, no merge conflict markers |
| Partial | Tag exists but commit message is uninformative |
| Zero | Tag absent or not pushed to remote |

---

## Strong Evidence Bonus (no extra points, but distinguishes borderline cases)

These items do not change the score category but are noted when a team is on the boundary between two levels:

- Standalone `docs/model-selection.md` with deeper analysis than the README table
- Architecture diagram updated to show fallback chain
- Hosting provider DPA link documented for OSS models
- Task-based routing implemented (routes simple tasks to cheaper model)
- Fallback activation test with captured log output showing secondary model used

---

## What Causes Automatic Deductions

- `.env` file committed to the repository: automatic zero on A6, flagged for security review
- Model name hardcoded as a string literal in production code (not read from environment): deduction on A2
- Benchmark results that are identical across all models (suggests copy-paste, not actual runs): flagged for discussion

---

## Resubmission Policy

One resubmission is allowed within one week of the original due date (by Thursday 11 June 2026 at 23:59) for up to 80% of lost points. Push a new commit and email zeshan.ahmad@kiu.edu.ge with the commit hash.

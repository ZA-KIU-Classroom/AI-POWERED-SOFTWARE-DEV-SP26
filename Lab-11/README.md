# Lab 11: Multi-Model Portability Sprint

**Course:** CS-AI-2025 — Building AI-Powered Applications, Spring 2026  
**Week:** 13 (Lab runs one week behind lecture)  
**Date:** Friday 29 May 2026  
**Group A:** 09:00 – 11:00 | **Group B:** 11:00 – 13:00  
**Homework Due:** Thursday 4 June 2026 at 23:59 Georgia Time  
**Git Tag:** `lab11-portability`

---

## What This Lab Is

This is a build lab, not a tutorial. You arrive with your capstone repository open and your terminal ready. By the end of the session you will have:

1. Benchmarked at least three models against your golden set and committed the results
2. Implemented a production fallback chain in your FastAPI backend
3. Written the model selection decisions table that the Repository Review grader looks for
4. Tagged your repository `lab11-portability` and pushed

The lecture introduced the theory. This lab is where you apply it to your actual capstone project.

---

## Prerequisites — Verify Before You Arrive Friday

Run these checks on Thursday evening. If any fail, fix them before the lab session starts.

```bash
# 1. Lab 10 tag exists and is pushed
git tag --list | grep lab10
# Expected: lab10-production

# 2. App runs locally
curl http://localhost:8000/health
# Expected: {"status": "ok", ...}

# 3. OpenRouter key works
python -c "
import os, openai
client = openai.OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=os.environ['OPENROUTER_API_KEY'],
)
print('Key prefix:', os.environ['OPENROUTER_API_KEY'][:8])
"

# 4. Golden set exists and has at least 5 questions
python -c "
import json
with open('eval/golden_set.json') as f:
    gs = json.load(f)
print(f'Golden set: {len(gs[\"questions\"])} questions')
assert len(gs['questions']) >= 5, 'Need at least 5 questions'
"

# 5. Golden set runner works
python eval/run_golden_set.py

# 6. Docker is installed
docker --version

# 7. Python version
python --version  # Should be 3.11 or 3.12
```

If `eval/golden_set.json` has fewer than 5 questions, add more before arriving. The benchmark script requires at least 5 to produce meaningful results.

---

## Session Plan

| Time | Activity | Duration |
|------|----------|----------|
| :00 | Arrival and prerequisite check | 5 min |
| :05 | Instructor opens — benchmark overview and session targets | 10 min |
| :15 | **Part 1:** Model benchmarking — run, score, commit | 25 min |
| :40 | **Part 2:** Fallback chain implementation and testing | 30 min |
| :70 | **Part 3:** README model selection table and cost analysis | 20 min |
| :90 | **Part 4:** Integration test — break the primary, verify fallback | 15 min |
| :105 | Commit, tag `lab11-portability`, push | 5 min |
| :110 | Wrap-up and Week 14 preview | 10 min |

---

## Deliverables — What the Grader Checks

### Required (must be present for full credit)

| Deliverable | Location in Repo | Notes |
|-------------|------------------|-------|
| Model benchmark results | `eval/model-comparison.json` | At least 3 models, at least 5 questions each |
| Fallback chain implementation | `backend/main.py` or equivalent | `chat_with_fallback()` function present and tested |
| `model_used` field in API responses | Your `/api/ai/chat` endpoint | Every response must include which model answered |
| Model selection decisions table | `README.md` | See template in `templates/model-selection-table.md` |
| Cost analysis update | `README.md` | Actual tokens spent last week + monthly projection |
| Git tag pushed | Remote `lab11-portability` | `git push origin main --tags` |

### Strong Evidence (distinguishes good from excellent)

| Deliverable | Notes |
|-------------|-------|
| `docs/model-selection.md` as standalone document | Linked from README, more detail than inline table |
| Architecture diagram updated to show fallback chain | In `docs/` or inline in README |
| Hosting provider DPA link | For any OSS model used via third-party host |
| Task-based routing implementation | Route simple tasks to cheaper model |
| Fallback activation test documented | Screenshot or log output showing secondary model responding |

---

## Homework

**Due: Thursday 4 June 2026 at 23:59 Georgia Time**

The homework for Lab 11 is committed to your repository, not submitted separately. The `lab11-portability` tag must point to a commit that includes all required deliverables.

---

## Course Links

- **Course GitHub:** [ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26](https://github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26)
- **Office Hours:** zeshan.ahmad@kiu.edu.ge — book via email for Google Meet
- **Week 14:** Thursday 4 June 2026 at 16:00 — Load testing, red teaming, jailbreak prevention + Peer Review Presentations

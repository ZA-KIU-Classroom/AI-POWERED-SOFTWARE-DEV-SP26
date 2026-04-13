# Lab 5 Grading Rubric

**Lab:** Lab 5 — Capstone Prototype Sprint
**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026
**Graded as:** Capstone progress checkpoint — feeds into Design Review and Repository Review scores
**Submission:** `lab5-checkpoint` tag pushed to team repo + individual `lab5-wrapup.md`

> Lab 5 does not have a standalone point value. It is a capstone progress checkpoint. The deliverables produced here feed directly into your **Design Review (10 pts)** and **Repository Review (10 pts)** scores. Falling behind in Lab 5 compounds into every subsequent capstone milestone.

---

## What the Instructor Checks After Lab 5

### Check 1: Design Decisions Document

**File:** `docs/design-decisions-lab5.md` in team repo
**Inspected for:**

| Criterion | Full Credit | Partial Credit | No Credit |
|---|---|---|---|
| Feedback acknowledgement | All Design Review feedback items are addressed — accepted or explicitly rejected with reasoning | Some items addressed, others missing | Document missing or empty |
| Change decisions | Clear statement of what is changing and what is not | Vague or generic statements | No decisions recorded |
| Prototype milestone | One specific, concrete feature named as the sprint target | Multiple vague goals | No milestone stated |

---

### Check 2: Working Prototype Endpoint

**Verified by:** Clone repo, add `.env`, run one command, send one request
**Inspected for:**

| Criterion | Passes | Fails |
|---|---|---|
| One-command startup | `uvicorn main:app` or `npm run dev` brings the app up with no errors | Errors on startup, missing dependencies, broken imports |
| Endpoint accepts real input | Route exists and accepts a POST body or equivalent | Route missing, 404, or requires manual code edits to run |
| Model call is real | Response comes from OpenRouter or Google AI Studio — not a mock, hardcoded string, or placeholder | Mocked or hardcoded response |
| Response is returned | Client receives the model output in a parseable format | 500 error, timeout, or no response body |

---

### Check 3: Cost Log

**File:** `logs/cost-log.md` or `logs/cost-log.csv` in team repo (or printed to terminal and captured)
**Inspected for:**

| Field | Required |
|---|---|
| Timestamp | Yes |
| Model name | Yes |
| Input token count | Yes |
| Output token count | Yes |
| Total latency (ms) | Yes |
| Calculated cost (USD) | Yes — use `(input / 1_000_000) * input_price + (output / 1_000_000) * output_price` |

At least three entries required — one from environment verification, at least two from the sprint.

---

### Check 4: Git Tag

**Command to verify:**

```bash
git tag | grep lab5-checkpoint
git show lab5-checkpoint --stat
```

The tag must exist and point to a commit that includes the design decisions document, the working endpoint code, and the cost log.

---

### Check 5: Individual Wrap-up Form

**Required from:** Every team member individually for Capstone Checkpoint #2
**Inspected for:** Completion — not content quality. Every field answered.

---

## Common Issues That Cost Points in Later Milestones

These are not graded today but they create debt you will pay later:

1. **`.env` committed to the repo.** Immediate -1.0 on Repository Review (Week 15). Add `.env` and `.env.local` to `.gitignore` now.

2. **No `README.md` update.** By Week 15, your repo needs a one-command setup script. Start the README today while setup is fresh.

3. **Cost log not started.** Week 11 Safety and Evaluation Audit requires a full cost history. Reconstructing it from memory is not accepted.

4. **Endpoint not covered by a test.** Not required today. But if you write the endpoint without a test, you will forget how it works in three weeks. Add even one `pytest` or `jest` test before you close the laptop.

5. **Team members without a working local environment.** Every team member must be able to run the project independently by Lab 6. Use the last 15 minutes to unblock anyone who is still stuck.

---

*Grading rubric for CS-AI-2025 Lab 5, Spring 2026.*

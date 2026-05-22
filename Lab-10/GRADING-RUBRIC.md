# Lab 10 Grading Rubric

**CS-AI-2025 · Building AI-Powered Applications · Spring 2026**

---

## How Lab 10 Is Assessed

Lab 10 has no standalone point value. The artifacts you build today are assessed as part of the **Repository Review (10 pts, Week 15)**. The grader opens your capstone repo at Week 15 and works through a checklist. Every item on that checklist that you complete today is points secured.

This rubric maps today's four parts directly to the Repository Review criteria.

---

## Part 1 — Secrets Audit

**Repository Review criterion:** No secrets in git history. `.env.example` present.

| Evidence | Points at Risk |
|----------|---------------|
| `git log --all -p \| grep -i "sk-or-"` returns no results | Up to 2 pts deducted if secrets found |
| `.env` is in `.gitignore` | Noted as a hard requirement |
| `.env.example` committed with placeholder values | Checked during repo review |
| `templates/secrets-audit-checklist.md` completed and committed | Demonstrates due diligence |

**What the grader does:** Runs the grep command against your repo history. Checks that `.env` is gitignored. Looks for `.env.example`. Any real credentials found in history result in immediate deductions regardless of other scores.

---

## Part 2 — GitHub Actions CI Workflow

**Repository Review criterion:** CI workflow present, passing, and gated on golden set score.

| Evidence | Points at Risk |
|----------|---------------|
| `.github/workflows/ci.yml` present in repo | Hard requirement |
| Workflow runs on push to main | Checked in workflow file |
| Golden set step present and threshold set at 0.70 | Checked in workflow file |
| Most recent workflow run shows green check | Checked in GitHub Actions tab |
| `eval/results/` contains at least one CI-generated results file | Checked in repo |

**What the grader does:** Opens the Actions tab. Checks the most recent run. Reads the workflow YAML. Looks for the threshold check step.

---

## Part 3 — Dockerfile and Health Endpoint

**Repository Review criterion:** One-command setup, Dockerfile builds, `/health` responds.

| Evidence | Points at Risk |
|----------|---------------|
| `backend/Dockerfile` present | Hard requirement |
| Dockerfile uses `python:3.11-slim` or equivalent non-root base | Checked in file |
| Non-root user configured in Dockerfile | Security baseline check |
| `HEALTHCHECK` instruction present in Dockerfile | Checked in file |
| `GET /health` returns `{"status": "ok"}` within 500ms | Grader runs this live |
| Health endpoint does not call the LLM | Checked by response time |

**What the grader does:** Runs `docker build -t test .` from the backend directory. Then `docker run -p 8000:8000 test`. Then `curl http://localhost:8000/health`. Times the response.

---

## Part 4 — Rate Limiter

**Repository Review criterion:** Rate limiting implemented, 429 response documented.

| Evidence | Points at Risk |
|----------|---------------|
| Rate limiting logic present in backend code | Checked in source |
| 429 response includes `retry_after_seconds` field | Checked in source |
| README documents the rate limiting behaviour | Checked in README |
| Model Selection Decisions table references rate limit choice | Checked in README |

**What the grader does:** Reads the rate limiting code. Looks for the 429 response contract. Checks the README for documentation of the behaviour.

---

## The Self-Assessment

Before Week 15, fill in `templates/repo-review-self-assessment.md` and commit it. This document shows the grader you did a systematic review and did not leave gaps. Teams that submit a completed self-assessment consistently score higher than teams that do not.

---

## Common Reasons Points Are Lost at Repository Review

1. **Secrets found in git history.** The grep command is run every time. There are no exceptions.
2. **Dockerfile present but does not build.** A broken Dockerfile is treated the same as no Dockerfile.
3. **`/health` calls the LLM.** The endpoint times out under health check conditions and causes the container to restart.
4. **CI workflow present but never green.** A workflow that has never passed suggests it was added for show, not function.
5. **Rate limiter in the code but not documented.** The grader looks for evidence you understand what you built, not just that the code is there.

---

*Lab 10 Grading Rubric · CS-AI-2025 · Spring 2026 · KIU*

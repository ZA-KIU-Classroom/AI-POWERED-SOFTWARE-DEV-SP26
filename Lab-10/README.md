# Lab 10: CI/CD and Production Hardening Sprint

**CS-AI-2025 · Building AI-Powered Applications · Spring 2026**
**Friday 22 May 2026 · Group A 09:00–11:00 · Group B 11:00–13:00**

---

## What This Lab Is

Lab 10 is a production hardening build session. There are no tutorials. There is no hand-holding through concepts you have not seen before. Everything in this lab was introduced in the Week 12 lecture on Thursday. Today you implement it on your capstone.

By the end of this lab your team will have shipped four production engineering artifacts into your capstone repository:

1. A secrets audit confirmation — no credentials in git history
2. A working GitHub Actions CI workflow that runs your golden set on every push to main and blocks deployment if the score drops below 0.70
3. A Dockerfile that builds and runs your FastAPI backend identically on any machine
4. A rate limiter that enforces per-user request limits and returns a structured 429 response

These artifacts are not graded today. They are read at the **Repository Review (10 pts, Week 15)**. The grader opens your repo and checks for them. If they are not there, points are not awarded. Today is the day to build them.

---

## Session Schedule

| Time | Activity | Duration |
|------|----------|----------|
| :00 | Arrival and prerequisite check | 5 min |
| :05 | Instructor opens — session targets | 5 min |
| :10 | Part 1: Secrets audit and .gitignore | 20 min |
| :30 | Part 2: GitHub Actions CI workflow | 30 min |
| :60 | Part 3: Dockerfile and health endpoint | 25 min |
| :85 | Part 4: Rate limiter | 15 min |
| :100 | Commit, tag `lab10-production`, push | 5 min |
| :105 | Wrap-up and Week 13 preview | 5 min |

*Group A runs 09:00 to 11:00. Group B runs 11:00 to 13:00.*

---

## Parts in Detail

### Part 1 — Secrets Audit and .gitignore (minutes 10–30)

Run the audit commands from `guides/secrets-audit.md` against your capstone repo. If you find any exposed keys, follow the remediation steps before doing anything else. Confirm `.env` is in `.gitignore` and commit a `.env.example` with placeholder values.

**Exit condition:** You can run `git log --all -p | grep -i "sk-or-"` and get no results.

### Part 2 — GitHub Actions CI Workflow (minutes 30–60)

Copy `starter-code/ci/ci.yml` into your repo at `.github/workflows/ci.yml`. Update the workflow to match your project structure. Confirm `OPENROUTER_API_KEY` is set in your repo's GitHub Secrets. Push to main and watch the Actions tab until the workflow goes green.

**Exit condition:** A green check appears on your most recent commit in GitHub.

### Part 3 — Dockerfile and Health Endpoint (minutes 60–85)

Copy `starter-code/docker/Dockerfile` into your `backend/` directory. Add the `/health` endpoint to your `main.py` using the pattern in `starter-code/docker/health_endpoint.py`. Build the image locally: `docker build -t capstone-app .`

**Exit condition:** `docker run -p 8000:8000 capstone-app` starts, and `curl http://localhost:8000/health` returns `{"status": "ok"}`.

### Part 4 — Rate Limiter (minutes 85–100)

Copy `starter-code/rate-limiter/rate_limiter.py` into your backend. Wire it into your chat endpoint using the pattern in `starter-code/rate-limiter/usage_example.py`. Test it manually by sending more than 10 requests in a minute and confirming the 429 response.

**Exit condition:** A rapid sequence of requests triggers a 429 with `retry_after_seconds` in the response body.

---

## The Commit and Tag

When all four parts are done:

```bash
git add -A
git commit -m "lab10: CI/CD and production hardening

- .github/workflows/ci.yml: golden set gate on every push to main
- Dockerfile: python:3.11-slim, non-root user, health check
- GET /health: returns status ok in under 100ms
- Rate limiter: 10 req/min per user, structured 429 response
- Secrets audit: no leaked keys in git history confirmed"

git tag lab10-production
git push origin main --tags
```

Confirm the tag is visible on GitHub before you leave. Go to your repo, click Tags, and verify `lab10-production` appears.

---

## Why This Matters for Your Final Grade

The Repository Review (10 pts) at Week 15 reads your repo as if hiring you. The grader runs a checklist that includes every artifact you build today:

- No secrets in git history
- `.github/workflows/ci.yml` present and passing
- `Dockerfile` present and builds without errors
- `GET /health` returns `{"status": "ok"}` within 500ms
- Rate limiting implemented — 429 response documented

Building these today is not optional polish. It is the engineering baseline that separates a portfolio-grade project from a prototype.

---

## Files in This Package

```
Lab-10/
├── README.md                          ← You are here
├── QUICKSTART.md                      ← Pre-session checklist
├── GRADING-RUBRIC.md                  ← Repository Review criteria this lab addresses
├── INSTRUCTOR-GUIDE.md                ← Word-for-word facilitation script with timing
├── guides/
│   ├── secrets-audit.md               ← Step-by-step git history audit and remediation
│   ├── github-actions-setup.md        ← Setting up Actions secrets and reading the logs
│   ├── docker-on-railway.md           ← Deploying your Docker image to Railway
│   └── fast-fixes.md                  ← Common errors and one-line solutions
├── starter-code/
│   ├── ci/
│   │   └── ci.yml                     ← Ready-to-use GitHub Actions workflow
│   ├── docker/
│   │   ├── Dockerfile                 ← Production Dockerfile for FastAPI
│   │   └── health_endpoint.py         ← Drop-in /health and /health/deep endpoints
│   └── rate-limiter/
│       ├── rate_limiter.py            ← Token bucket implementation
│       └── usage_example.py           ← How to wire the rate limiter into FastAPI
└── templates/
    ├── env-example.md                 ← Template for your .env.example file
    ├── secrets-audit-checklist.md     ← Fill-in checklist to commit with your repo
    └── repo-review-self-assessment.md ← Self-assessment against the Week 15 rubric
```

---

## Getting Help

- **Docker not installed:** See `guides/fast-fixes.md` — install takes 3 minutes on Mac/Linux
- **GitHub Actions failing:** Check the Actions tab in your repo for the error log. Common fixes in `guides/github-actions-setup.md`
- **Rate limiter import error:** Confirm `fastapi` is in `requirements.txt`
- **Health endpoint returning 500:** Your app has a startup error — check `uvicorn` logs
- **Office hours:** zeshan.ahmad@kiu.edu.ge — book via email for Google Meet

---

*Lab 10 · CS-AI-2025 · Spring 2026 · KIU*

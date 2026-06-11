# Final Repo Checklist — CS-AI-2025

**Course:** Building AI-Powered Applications | Spring 2026
**Repo freeze:** Wednesday 10 June 2026 at 23:59 (Tbilisi time, UTC+4)
**Demo Day:** Thursday 11 June 2026 at 16:00
**Repository Review due:** Sunday 14 June 2026 at 23:59

> Graders read your repository, not your laptop. The state of your main branch at the freeze deadline is what is scored. No commits after Wednesday 23:59 count toward Repository Review.

---

## Hard Gates — Pass or Fail

Fail any one of these and your Repository Review score is capped. Check these first, before anything else.

- [ ] No secrets in git history — run `git log --all -p | grep -i "sk-or-"` and confirm it returns nothing. Deleting a file in a later commit does not remove it from history. If you find a hit, rewrite history with `git filter-repo` or rotate the key and document that you did so in your README.
- [ ] `Dockerfile` builds and runs from a clean checkout — test with `docker build -t myapp . && docker run myapp` on a machine that has never seen your code before.
- [ ] `GET /health` responds under 500ms — this endpoint must NOT call the LLM. It should check internal state only.
- [ ] CI workflow is green on main branch — `.github/workflows/ci.yml` must show a passing run, not a skipped one.
- [ ] `eval/results/` has at least 3 committed run files — they must be in git, not just on your local machine.

---

## Git Tags — Push All Four Before Freeze

All four tags must be pushed to your remote before Wednesday 23:59. Run `git tag` locally and compare against this list. Missing tags cannot be added after the freeze.

```bash
# Verify which tags you have pushed
git ls-remote --tags origin

# Push any missing tags
git tag lab9-hardening       # if not already tagged
git tag lab10-production     # if not already tagged
git tag lab11-portability    # if not already tagged
git tag lab12-demo-day       # tag your final state before freeze

git push origin --tags
```

| Tag | Lab | What it marks |
|---|---|---|
| `lab9-hardening` | Lab 9 | Golden set written, eval harness running, safety audit evidence committed |
| `lab10-production` | Lab 10 | Dockerfile, CI, `/health`, rate limiter, fallback chain all in place |
| `lab11-portability` | Lab 11 | Model comparison committed, fallback chain using `.env` model names, portability complete |
| `lab12-demo-day` | Lab 12 | Final freeze state: videos embedded, case study written, all docs complete |

> A tag points to a specific commit. If you tag and then keep committing, the tag does not move. Tag last, after everything else is done.

---

## High Priority — Post-Safety-Audit Work (Labs 9 to 12)

This section covers the majority of the remaining points. Work through it in order.

### Evaluation

- [ ] `eval/golden_set.json` — 10 questions present: 3 factual, 2 reasoning, 2 edge case, 2 refusal, 1 format
- [ ] `eval/run_golden_set.py` — runs clean in under 3 minutes, 7 or more of 10 must pass (0.70 threshold)
- [ ] `eval/model-comparison.json` — 3 or more models benchmarked, 5 or more questions each
- [ ] 3 or more result files committed to `eval/results/`

### Production Engineering

- [ ] `.github/workflows/ci.yml` — golden set gate enforced at 0.70 threshold, `OPENROUTER_API_KEY` stored in GitHub Secrets (not hardcoded)
- [ ] `Dockerfile` — non-root user, `HEALTHCHECK` instruction included, base image is `python:3.11-slim`
- [ ] Rate limiter on chat endpoint — returns a structured 429 response with a `retry_after_seconds` field
- [ ] Fallback chain in place (`PRIMARY` then `SECONDARY` then `OSS_FALLBACK`) — all model names read from `.env`, never hardcoded in source
- [ ] Every API response includes a `model_used` field
- [ ] Every episode log entry includes `model_used` and `fallback_triggered`

### Load Test and Red Team

- [ ] `load/locustfile.py` — run against your deployed app at 50 users for 2 minutes
- [ ] `load/load-test-report.md` — contains real p50, p95, and p99 latency numbers, throughput, and error rate from the run above
- [ ] 4 red-team attacks documented in `docs/safety-audit.md`: prompt injection, indirect injection, jailbreak, and data exfiltration — each entry must include the exact input used, what the model did, and which control held

### Videos and Demo Day

- [ ] 2-minute narrated demo video — embedded or linked in `README.md`, link must be publicly accessible without login
- [ ] 60-second launch video — plays first at Demo Day, ready on the presenter laptop before 16:00
- [ ] 8-slide deck ready, rehearsed, and fits within the 10-minute talk slot

### Documentation

- [ ] `docs/safety-audit.md` — all 6 audit areas complete, Lab 12 red-team section appended
- [ ] `docs/case-study.md` — 2 to 3 pages covering: problem, approach, results, lessons learned
- [ ] `README.md` model selection table — columns: task, model, reason, fallback, real cost numbers
- [ ] `AGENTS.md` present in repo root

---

## Overall Completeness — Whole Repo

- [ ] `README.md` — contains: overview, architecture diagram or description, setup instructions, eval results summary table, cost breakdown, and the 2-minute demo video embedded or linked
- [ ] `TEAM-CONTRACT.md` — signed by all team members
- [ ] `.env.example` — all variable names present with placeholder values, real `.env` never committed, `.env` listed in `.gitignore`
- [ ] `docs/design-review/DESIGN-REVIEW.md` — no `[fill in]` placeholders remaining anywhere in the file
- [ ] `docs/agent-architecture-lab7.md` — pattern chosen and documented, `AgentState` is typed, irreversible actions mapped to guards
- [ ] `docs/optimization-report.md` — prompt caching benchmark with before and after numbers
- [ ] `docs/data-map.md` — documents what is stored, where it is stored, retention policy, and how a user can request deletion
- [ ] `docs/metrics-report.md` — 6 metrics from the episode log with pass/fail thresholds defined
- [ ] `logs/episode-log.jsonl` — 100 or more entries, full schema present, zero PII in any entry
- [ ] `mcp-server/` — bearer token auth, Pydantic validation, structured logging, sanitised error responses
- [ ] All 4 lab git tags pushed (see Git Tags section above)
- [ ] Every team member has commits spread across the full semester, not just the final week

---

## Expected Directory Structure

Your repository should match this structure closely. Graders will look for files at these exact paths.

```
your-team-repo/
├── README.md                          # overview, architecture, setup, eval results, cost, 2-min video
├── AGENTS.md                          # AI coding agent guide — how to work in this repo
├── TEAM-CONTRACT.md                   # signed by all members
├── .env.example                       # all variable names, no values
├── .gitignore                         # .env must be listed here
├── Dockerfile                         # non-root user, HEALTHCHECK, python:3.11-slim base
├── docker-compose.yml                 # optional but recommended
├── .github/
│   └── workflows/
│       └── ci.yml                     # golden set gate at 0.70, OPENROUTER_API_KEY secret
├── src/  (or app/)                    # your application code
│   └── main.py  (or equivalent)
├── eval/
│   ├── golden_set.json                # 10 questions: 3 factual, 2 reasoning, 2 edge, 2 refusal, 1 format
│   ├── run_golden_set.py              # runs in under 3 min, 7+ of 10 must pass
│   ├── model-comparison.json          # 3+ models, 5+ questions each
│   └── results/
│       ├── run_001.json               # at least 3 separate committed run files
│       ├── run_002.json
│       └── run_003.json
├── load/
│   ├── locustfile.py                  # 50 users, 2 min run
│   └── load-test-report.md            # real p50/p95/p99, throughput, error rate
├── logs/
│   └── episode-log.jsonl              # 100+ entries, full schema, zero PII
├── mcp-server/                        # bearer token auth, Pydantic validation, sanitised errors
├── docs/
│   ├── safety-audit.md                # all 6 areas + Lab 12 red-team section
│   ├── case-study.md                  # 2 to 3 pages: problem, approach, results, lessons
│   ├── agent-architecture-lab7.md     # pattern, typed AgentState, irreversible action guards
│   ├── optimization-report.md         # prompt caching before/after benchmark
│   ├── data-map.md                    # what is stored, where, retention, deletion
│   ├── metrics-report.md              # 6 metrics with pass/fail thresholds
│   └── design-review/
│       └── DESIGN-REVIEW.md           # no [fill in] placeholders remaining
└── templates/
    └── repo-review-checklist.md       # your self-assessment against this checklist
```

---

## Priority Order for the Final Push

Work through this in sequence. Each item closes a hard gate, earns audit points, or feeds your Demo Day slides directly.

1. Run the golden set and commit 3 result files — closes the hard gate, earns audit points, and gives you real numbers for the measurements slide
2. Confirm CI is green, Dockerfile builds, and `/health` responds correctly — hard gates
3. Secrets audit — run the grep command above and fix any hits before anything else
4. Append red-team results to `docs/safety-audit.md`
5. Shoot and embed the 2-minute narrated demo video in `README.md`
6. Cut the 60-second launch video
7. Lock the model selection table and cost numbers in `README.md`
8. Write `docs/case-study.md`
9. Push all 4 lab tags
10. **Freeze repo: Wednesday 10 June at 23:59**

---

## How This Maps to the Grade

| Graded item | Points | What this checklist feeds |
|---|---|---|
| Demo Day | 15 | Videos section, 8-slide deck, real numbers from eval and load test |
| Repository Review | 10 | Every section of this checklist |
| **Total at stake** | **25** | |

---

*CS-AI-2025 Building AI-Powered Applications | Spring 2026 | Instructor: Zeshan Ahmad*

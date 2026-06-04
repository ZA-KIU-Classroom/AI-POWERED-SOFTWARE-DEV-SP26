# Lab 12 · The Final Sprint

**Course:** CS-AI-2025 · Building AI-Powered Applications · Spring 2026
**Lecture pairing:** Week 14 · Harden It, Then Ship It
**Lab date:** Friday 5 June 2026 · Group A 09:00 · Group B 11:00
**Instructor:** Zeshan Ahmad · zeshan.ahmad@kiu.edu.ge
**Repository:** `github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26`

---

## What this lab is

This is your last lab before Demo Day. It is a supported work session, not a graded checkpoint. There is no graded deliverable in this lab. The point is to do the Demo Day preparation here, with the instructor in the room to help and to act as your first hostile reviewer, so that nothing is left to scramble for in the final week.

You work on three things, in parallel, by splitting your team:

1. **The Demo Day presentation and video.** Build the required 8-slide deck, shoot the 2-minute narrated demo video, and cut the 60-second launch video.
2. **Hardening.** Run a Locust load test against your deployed app, then red team it with prompt injection, a jailbreak, and a poisoned document.
3. **Repository Review prep.** Close the hard gates and assemble the portfolio. The Repository Review is now worth **15 points**, the largest single block of points left, so this is not busywork.

You leave with a prioritised fix list and a repo that is close to frozen.

## Where the points are now

To be clear about what is and is not graded:

- This lab has **no graded item**. It is preparation time.
- **Demo Day (15 pts)** is graded in Week 15.
- **Repository Review (15 pts)** is graded in Week 15.
- **Peer Assessment (5 pts)** is an individual contribution form you complete at the end of the year. It is not done in this lab.

## Learning goals

By the end of Lab 12 you will be able to:

- Run a Locust load test against your deployed backend and interpret p50, p95, and p99 latency, throughput, and error rate.
- Red team your own app with the four core attacks and document each result and the control that stopped it.
- Build the required Demo Day deck and have a first cut of both videos.
- Close every Repository Review hard gate and know exactly what remains for the portfolio.

## Session shape

The session is 120 minutes. It is a work session, so there is no rigid timetable. The instructor walks the room, helps, and pressure-tests each team. A suggested rhythm is in `INSTRUCTOR-GUIDE.md`.

| Block | Focus |
|---|---|
| Arrival | Warm up your deployed app, split your team across the three workstations |
| Main work | Deck and video, hardening, and repo prep run in parallel |
| Instructor rounds | The instructor tries to break your app and opens your repo against the gates |
| Wrap | Each team commits its work and writes a ranked Demo Day fix list |

## What you produce during this lab

These are working artifacts for your own Demo Day and Repository Review preparation. None of them is a graded homework.

- `load/locustfile.py` (start from `examples/locustfile.py`) and `load/load-test-report.md` (use `templates/load-test-report.md`)
- An updated `docs/safety-audit.md` with this week's red-team results (use `templates/safety-audit.md`)
- A first cut of the Demo Day deck and the demo video
- `docs/demo-day-fix-list.md` (use `templates/demo-day-fix-list.md`)
- A completed `templates/repo-review-checklist.md` so you know exactly which gates are closed
- Recommended checkpoint tag: `lab12-hardening` (optional, marks your hardened state)

## Prerequisites already in your repo from earlier labs

This lab builds directly on Lab 11. Before you arrive you should already have:

- A deployed, reachable FastAPI backend with `/api/chat` and a `/health` endpoint
- An OpenRouter fallback chain (`PRIMARY_MODEL`, `SECONDARY_MODEL`, `OSS_FALLBACK` in your `.env`) with a `model_used` field on every response
- `eval/golden_set.json` with at least 5 questions and `eval/model-comparison.json` from Lab 11
- An existing `docs/safety-audit.md` from the Week 11 Safety and Evaluation Audit

If any of these are missing, read `QUICKSTART.md` first and fix them in the first few minutes.

## Package contents

```
Lab-12/
  README.md                         this file
  QUICKSTART.md                     the 5-minute pre-lab checklist
  GRADING-RUBRIC.md                 what this week's work is graded against (Demo Day + Repository Review)
  INSTRUCTOR-GUIDE.md               facilitation flow for the work session, probing questions
  templates/
    safety-audit.md                 red-team documentation, append to docs/safety-audit.md
    load-test-report.md             where to record your Locust results
    demo-day-fix-list.md            the prioritised action list you leave with
    repo-review-checklist.md        the 15-point Repository Review gate and portfolio tracker
  guides/
    load-testing-with-locust.md     install, run, and read a load test
    red-teaming-your-app.md         the attack playbook and the four defenses
    presentation-checklist.md       the 8-slide deck, the videos, and the live-demo rules
  examples/
    locustfile.py                   runnable Locust starter for your backend
    attacks.md                      concrete attack strings to try
    sample-safety-audit.md          a filled-in example so you see the bar
```

## After this lab

There is no graded homework. From Friday to Demo Day your only job is to finalise:

1. Shoot the 2-minute narrated demo video, then cut the 60-second launch video.
2. Close every Repository Review hard gate (see `templates/repo-review-checklist.md`).
3. Rehearse the 10-minute talk with a timer so you do not run over.
4. Freeze the repo by **Wednesday 10 June at 23:59**. Graders read your git history, not your laptop.

**Demo Day is Thursday 11 June at 16:00.** Ten-minute talk, five-minute Q&A.

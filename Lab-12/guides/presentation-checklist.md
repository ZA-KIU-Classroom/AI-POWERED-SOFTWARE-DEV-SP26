# Guide · The Demo Day Presentation Checklist

This is the format you prepare in Lab 12 and deliver in Week 15. Demo Day is **Thursday 11 June at 16:00**: a **10-minute talk** plus a **5-minute Q&A** per team. Use this guide to build the deck and run the live demo.

## The required 8-slide deck

Eight slides, no more. The times are a guide for your 10-minute slot.

| # | Slide | Time | What it must show |
|---|---|---|---|
| 1 | Title | 0:30 | Team, product name, one-line value. Open by playing your 60-second launch video. |
| 2 | Problem and user | 1:30 | One concrete user, their pain, why it matters now. |
| 3 | What it does | 1:00 | The single core capability you nail. Not a feature list. |
| 4 | Live demo | 3:00 | The deployed product itself, scripted happy path, backup recording ready. |
| 5 | Architecture | 1:30 | One diagram: the Perceive, Reason, Act, Observe loop, your stack, model and fallback. |
| 6 | Measurements | 1:00 | Golden-set score, p95 latency, cost per request, load-test result. Real numbers. |
| 7 | Safety and reliability | 0:30 | Threat model in one line each: attacks run, guardrails that held, failure path. |
| 8 | Lessons and next | 0:30 | One honest lesson, one thing you would build next. |

That is about 9 minutes of content with a minute of buffer. The launch video plays inside slide 1, so it costs no extra time.

## The two videos, do not confuse them

| | Launch video | Demo video |
|---|---|---|
| Length | 60 seconds | 2 minutes |
| Format | Vertical 9:16, social style | Horizontal screen recording |
| Goal | Make people want it | Prove it works |
| Lives in | Plays first at Demo Day, committed to repo | Embedded in your README |
| Graded under | Demo Day, 15 pts | Repository Review, 15 pts |

Shoot the 2-minute demo video first, then cut the punchy 60-second launch clip from your best moments.

## Live demo rules

**Do:** script the exact happy path and rehearse it; warm the app before your slot; use seeded demo data; keep a backup recording one click away; have one teammate drive while another narrates.

**Never:** live-code or edit config on stage; demo an untested feature; depend on room wifi for a heavy upload; type long prompts live; improvise when it breaks. If the live demo fails for more than 10 seconds, say "let me show you the recording" and cut to the backup. A calm switch looks professional.

## Repository Review hard gates (due Week 15)

These are pass or fail. Close them before the Wednesday 10 June freeze.

- [ ] No secrets anywhere in git history (deleting the file later does not clear history)
- [ ] Working Dockerfile that builds and runs
- [ ] `/health` endpoint responds under 500ms
- [ ] Green CI run on the main branch
- [ ] `eval/results/` with at least 3 committed run files

## The portfolio that earns the points

- One-command setup that runs from a clean clone
- README with overview, architecture, setup, eval results, and cost
- The 2-minute demo video embedded in the README
- A 2 to 3 page case study: problem, approach, results, lessons
- `AGENTS.md` so AI coding agents know how to work in your repo
- A live deployed URL (bonus)

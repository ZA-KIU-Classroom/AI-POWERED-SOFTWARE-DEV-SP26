# What This Week's Work Is Graded Against

Lab 12 itself is not graded. It is the work session where you prepare for the two graded items in Week 15. This file is your target: it is exactly how Demo Day and the Repository Review are scored, so you know what your Friday work is building toward.

There is also a separate **Peer Assessment (5 points)**, an individual contribution form completed at the end of the year. It is not part of this lab and is not a presentation.

---

## Demo Day (15 points)

Each team gets a 10-minute talk and a 5-minute Q&A in Week 15. Scored on four equal dimensions.

| Dimension | Weight | Points | What it measures |
|---|---|---|---|
| Real user value | 25% | 3.75 | Does it solve a real problem for a real user? |
| Robustness | 25% | 3.75 | Load tested, red teamed, graceful failure paths |
| Measurements | 25% | 3.75 | Golden-set results, latency, cost. Real numbers |
| Storytelling | 25% | 3.75 | The launch video, the narrative, the live demo |
| **Total** | **100%** | **15** | |

What a strong Demo Day shows: one concrete user and the pain you remove; evidence that you load tested and red teamed; real numbers for score, latency, and cost; and a clean live demo opened by your 60-second launch video. Two of these four dimensions, robustness and measurements, are exactly the hardening work you do in this lab.

---

## Repository Review (15 points)

Worth 15 points, due Week 15. This is the largest single block of points left in the course. It has two parts: hard gates that are pass or fail, and a portfolio that earns the points. Graders read your repository, not your laptop. Track your progress in `templates/repo-review-checklist.md`.

### Hard gates · pass or fail

- No secrets anywhere in git history, not just the latest commit
- A working Dockerfile that builds and runs
- A `/health` endpoint that responds under 500ms
- A green CI run on the main branch
- `eval/results/` with at least 3 committed run files

A secret in any past commit fails the gate even if you deleted it later. Rewrite history or rotate the key.

### Portfolio · earns the points

- One-command setup that runs from a clean clone
- README with overview, architecture, setup, eval results, and cost
- The 2-minute narrated demo video embedded in the README
- A 2 to 3 page case study: problem, approach, results, lessons
- `AGENTS.md` so AI coding agents know how to work in your repo
- A deployed app with a live URL (bonus)

---

## How Friday maps to the grade

| Friday workstation | Feeds which graded item |
|---|---|
| Demo Day deck and videos | Demo Day storytelling, and the demo video also lives in the Repository Review portfolio |
| Load test and red team | Demo Day robustness and measurements, and the safety audit in the portfolio |
| Repository Review prep | The full 15-point Repository Review |

Every minute of this lab moves a real graded number. Use the instructor as your first hostile reviewer before the judges are.

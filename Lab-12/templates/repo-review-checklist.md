# Repository Review Checklist (15 points)

Commit this to `docs/repo-review-checklist.md` and tick items as you close them. The Repository Review is worth 15 points in Week 15, the largest single block left. Graders read your repository, not your laptop, so if it is not committed it does not count.

## Hard gates · pass or fail

These must all pass. A single failure here caps your score regardless of the portfolio.

- [ ] No secrets anywhere in git history (run a history scan, not just a look at the latest commit)
- [ ] Working Dockerfile that builds and runs from a clean checkout
- [ ] `/health` endpoint responds under 500ms (confirmed with your load test, not assumed)
- [ ] Green CI run on the main branch
- [ ] `eval/results/` contains at least 3 committed run files

### Evidence for each gate

| Gate | How you verified it | Pass? |
|---|---|---|
| No secrets in history | | |
| Dockerfile builds and runs | | |
| /health under 500ms | | |
| Green CI on main | | |
| 3+ eval run files committed | | |

## Portfolio · earns the points

- [ ] One-command setup that runs from a clean clone (a script or a single documented command)
- [ ] README: overview, architecture, setup, evaluation results, and cost analysis
- [ ] The 2-minute narrated demo video embedded in the README
- [ ] A 2 to 3 page case study: problem, approach, results, lessons learned
- [ ] `AGENTS.md` so AI coding agents know how to work in your repo
- [ ] Model selection decisions table in the README (from Lab 11)
- [ ] Data governance note: which data goes to which provider and under what retention
- [ ] Deployed app with a live URL (bonus)

## If a secret is in your history

Deleting the file in a later commit does not remove it from history. Either rewrite history to purge it, or rotate the exposed key immediately and confirm the old one is dead. Do this before the Wednesday 10 June freeze.

## Freeze

- [ ] Everything above committed and pushed by Wednesday 10 June at 23:59

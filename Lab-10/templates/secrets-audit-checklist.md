# Secrets Audit Checklist

**Team:** _______________________________________________
**Date:** 22 May 2026
**Completed by:** _______________________________________________

Commit this file to your capstone repo after completing Lab 10 Part 1.
File path: `docs/secrets-audit-checklist.md`

---

## Audit Commands Run

```bash
# Record the output of each command below.
# "No output" is the correct result for all three.

git log --all --full-history -p | grep -i "sk-or-"
# Result: _______________________________________________

git log --all -p | grep -E "(api_key|OPENROUTER|secret|token|password)\s*=\s*['\"][^'\"]{10,}"
# Result: _______________________________________________

git log --all --full-history -- "*.env"
# Result: _______________________________________________
```

---

## Findings and Remediation

**Was any secret found in git history?**
- [ ] No — history is clean
- [ ] Yes — remediation completed (describe below)

**If yes, describe what was found and what was done:**

```
Finding: _______________________________________________

Remediation steps taken:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Key rotated on: _______________________________________________
git filter-repo run on: _______________________________________________
Force push completed: _______________________________________________
Team members re-cloned: _______________________________________________
```

---

## .gitignore Verification

**Does .gitignore exist at the repo root?**
- [ ] Yes

**Does .gitignore contain `.env`?**
- [ ] Yes

**Does .gitignore contain `venv/` or `.venv/`?**
- [ ] Yes

**Does .gitignore contain `__pycache__/`?**
- [ ] Yes

**Does .gitignore contain `*.pyc`?**
- [ ] Yes

---

## .env.example Verification

**Is `.env.example` committed to the repo root?**
- [ ] Yes

**Does it contain placeholder values only (no real keys)?**
- [ ] Yes

**Does it list every variable that `os.environ` or `os.getenv` reads?**
- [ ] Yes

---

## Sign-Off

By completing and committing this checklist, the team confirms that:
- The git history audit was run and no unexpired secrets were found (or found secrets were rotated and removed)
- The `.env` file is gitignored and no real credentials are committed
- `.env.example` is committed with placeholder values

**Team members who reviewed this audit:**

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

*Secrets Audit Checklist · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*

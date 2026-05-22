# Lab 10 Quickstart

**This lab is a build session, not a tutorial. Everything here was taught in the Week 12 lecture. Come ready to implement.**

---

## Before You Arrive — Thursday Evening or Friday Morning

### 1 — Confirm Your App Runs Locally

```bash
cd backend
uvicorn main:app --reload
curl http://localhost:8000/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "conversation_history": []}'
```

If this does not return a response, fix it before the lab. Parts 3 and 4 both require a running app.

### 2 — Confirm Docker Is Installed

```bash
docker --version
```

If Docker is not installed, install it now — not during the lab. Go to [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) and follow the instructions for your OS. The install takes 3–5 minutes.

### 3 — Confirm Your Golden Set Runs

```bash
python eval/run_golden_set.py
```

Part 2 wires your golden set into GitHub Actions. If it does not run locally, it will not run in CI. Fix any errors before Friday.

### 4 — Add OPENROUTER_API_KEY to GitHub Secrets

Go to your capstone repo on GitHub:

```
Settings → Secrets and variables → Actions → New repository secret
Name:  OPENROUTER_API_KEY
Value: your actual key
```

The CI workflow will fail at the golden set step if this secret is not present. Do it tonight.

### 5 — Run the Secrets Pre-Audit

Run this command against your capstone repo before the lab:

```bash
git log --all --full-history -p | grep -i "sk-or-"
```

If this returns anything, rotate your OpenRouter key now and read `guides/secrets-audit.md` for the full remediation steps. Do not wait until the lab to discover this.

---

## The Morning of the Lab — Friday 22 May

Arrive 5 minutes before your group starts. Open four things before the session begins:

1. Your terminal with the app running — `uvicorn main:app --reload`
2. Your capstone repo open in your editor
3. Your capstone repo open in GitHub (for the Actions tab in Part 2)
4. This README and the starter code in `starter-code/`

---

## Session Playbook

```
Minutes 0–5:   Arrival — confirm four things above are ready
Minutes 5–10:  Instructor opens — targets and common blockers
Minutes 10–30: Part 1 — secrets audit and .gitignore
Minutes 30–60: Part 2 — GitHub Actions CI workflow
Minutes 60–85: Part 3 — Dockerfile and health endpoint
Minutes 85–100: Part 4 — rate limiter
Minutes 100–105: Commit, tag lab10-production, push
Minutes 105–110: Wrap-up and Week 13 preview
```

---

## What the Tag Proves

The `lab10-production` tag is your evidence marker. When the Repository Review runs at Week 15, the grader checks that these files exist in your repo at or after the tag commit:

- `.github/workflows/ci.yml`
- `backend/Dockerfile`
- `GET /health` endpoint in your code
- Rate limiting logic in your backend
- No secrets in git history (verified by the audit)

Push the tag before you leave the lab.

---

*Lab 10 Quickstart · CS-AI-2025 · Spring 2026 · KIU*

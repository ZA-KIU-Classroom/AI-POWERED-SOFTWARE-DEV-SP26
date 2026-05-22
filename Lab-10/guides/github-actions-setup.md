# GitHub Actions Setup Guide

Everything you need to get your CI workflow running and read what it tells you.

---

## Step 1 — Add Your Secret to GitHub

Your workflow calls OpenRouter. GitHub needs your key to do that.

1. Go to your capstone repo on GitHub
2. Click **Settings** (top navigation, not your account settings)
3. In the left sidebar, click **Secrets and variables**, then **Actions**
4. Click **New repository secret**
5. Name: `OPENROUTER_API_KEY`
6. Value: your actual OpenRouter key (starts with `sk-or-`)
7. Click **Add secret**

The secret is now encrypted and available to your workflow as `${{ secrets.OPENROUTER_API_KEY }}`. It is never visible in logs.

---

## Step 2 — Copy the Workflow File

Copy `starter-code/ci/ci.yml` from this lab package into your capstone repo at exactly this path:

```
your-capstone-repo/
└── .github/
    └── workflows/
        └── ci.yml
```

The `.github/` directory goes at the root of your repo, not inside `backend/` or `frontend/`.

```bash
# From your capstone repo root
mkdir -p .github/workflows
cp /path/to/Lab-10/starter-code/ci/ci.yml .github/workflows/ci.yml
```

Open the file and update these two lines to match your project:

```yaml
# Line that installs dependencies — adjust if your requirements file is elsewhere
run: pip install -r backend/requirements.txt

# Line that runs the golden set — adjust if your script path is different
run: python eval/run_golden_set.py --output eval/results/ci-run.json
```

---

## Step 3 — Push and Watch the Run

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add golden set gate workflow"
git push origin main
```

Then:

1. Go to your repo on GitHub
2. Click the **Actions** tab
3. You should see a workflow run appear within 10 seconds of pushing
4. Click the run to watch it in real time

A passing run shows green checkmarks on every step. A failing run shows a red X on the step that failed.

---

## Reading the Actions Log

Click on any step in the run to expand its log output. Here is what to look for:

**If "Install dependencies" fails:**
```
ERROR: Could not find a version that satisfies the requirement xyz
```
A package in your `requirements.txt` does not exist or has a typo. Fix the package name locally and push again.

**If "Run golden set evaluation" fails:**
```
FileNotFoundError: eval/run_golden_set.py
```
The path to your golden set script is wrong relative to the repo root. Check where your `eval/` folder actually lives and update the workflow path.

```
KeyError: OPENROUTER_API_KEY
```
The secret is not set. Go back to Step 1.

**If "Check golden set threshold" fails:**
```
Score: 60%
FAIL: below 0.70 threshold
```
Your golden set score is genuinely below 0.70. This is real information. Your agent is failing too many evaluation questions. Review which questions are failing and address them before Demo Day.

---

## Making the Workflow Pass on Every Future Push

The workflow runs automatically on every push to `main`. That means:

- Every prompt change you make will be tested automatically
- Every model swap will be tested automatically
- Every code change that touches the response logic will be tested automatically

If a push causes a failure, the Actions tab shows a red X on that commit in your repo's commit history. Fix the underlying issue and push again.

**The goal by Week 15:** every commit in your recent history shows a green check. That is what Demo Day-ready looks like.

---

*GitHub Actions Setup Guide · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*

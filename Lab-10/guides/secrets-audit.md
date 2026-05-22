# Secrets Audit Guide

**Run this guide before doing anything else in Lab 10.**

---

## Step 1 — Search Your Full Git History

Run these commands from the root of your capstone repo:

```bash
# Search for OpenRouter API keys
git log --all --full-history -p | grep -i "sk-or-"

# Search for any pattern that looks like a key assignment
git log --all -p | grep -E "(api_key|OPENROUTER|secret|token|password)\s*=\s*['\"][^'\"]{10,}"

# List every .env file ever committed, including deleted ones
git log --all --full-history -- "*.env"
git log --all --full-history -- ".env"
```

**If all three commands return no output:** your history is clean. Move to Step 3.

**If any command returns output:** move to Step 2 immediately before pushing anything.

---

## Step 2 — Remediate a Leaked Secret

### 2a — Rotate the Key First

Go to [openrouter.ai](https://openrouter.ai), sign in, go to Account → API Keys. Revoke the exposed key and generate a new one. Do this before anything else. A key that is in git history and has not been rotated is still live.

Update your `.env` file with the new key.

### 2b — Remove the Key from History

```bash
# Install git-filter-repo if you do not have it
pip install git-filter-repo --break-system-packages

# Remove .env from all history
git filter-repo --path .env --invert-paths

# If the key was hardcoded in a .py file, use this instead
# Replace 'your-old-key-value' with the actual key string
git filter-repo --replace-text <(echo "your-old-key-value==>REDACTED")
```

### 2c — Force Push All Branches

```bash
git push --force --all
git push --force --tags
```

**Important:** every collaborator on your team must delete their local clone and re-clone after this. Their local copies still contain the secret.

### 2d — Update GitHub Secrets

Go to your repo on GitHub → Settings → Secrets and variables → Actions. If the old key was stored there, update it with the new rotated key.

### 2e — Verify the Fix

Run the original grep command again. It must return no output before you proceed.

```bash
git log --all --full-history -p | grep -i "sk-or-"
```

---

## Step 3 — Verify .gitignore

Open your `.gitignore` file at the repo root. Confirm it contains at minimum:

```
.env
.env.*
*.env
__pycache__/
.venv/
venv/
node_modules/
*.pyc
```

If `.env` is not listed, add it now:

```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: ensure .env is gitignored"
```

---

## Step 4 — Commit a .env.example

Your `.env.example` tells future collaborators (and the Repository Review grader) what environment variables are required. It contains placeholder values only — never real keys.

Create or update it:

```bash
cat > .env.example << 'EOF'
# Copy this file to .env and fill in your real values
# Never commit your real .env file

OPENROUTER_API_KEY=your-openrouter-key-here
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET=your-jwt-secret-here
REDIS_URL=redis://localhost:6379
EOF

git add .env.example
git commit -m "chore: add .env.example with placeholder values"
git push
```

---

## Step 5 — Fill in the Audit Checklist

Open `templates/secrets-audit-checklist.md`, complete every line, and commit it to your repo. This document is evidence of due diligence at the Repository Review.

---

## Common Questions

**"I found a key but it is from three months ago and already expired. Do I still need to remove it?"**
Yes. The Repository Review runs the grep command regardless of key age. Remove it.

**"My teammate committed the key, not me. Is it still my problem?"**
Yes. It is in your shared repo. Fix it together.

**"git filter-repo says 'fatal: not a git repository'."**
You are running the command from the wrong directory. Run it from the root of your capstone repo.

**"After force pushing, my Actions workflow shows old failed runs. Is that okay?"**
Yes. The old runs reflect the old history. New runs after the force push will reflect the clean history.

---

*Secrets Audit Guide · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*

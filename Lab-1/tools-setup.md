# Tools Setup Guide

**Complete environment setup for CS-AI-2025 Lab 1**  
*If you are already set up, go directly to [`quickstart.md`](../quickstart.md).*

This guide covers everything from a blank machine to a fully configured AI development environment. Follow each section in order. The setup should take 20–30 minutes on a fresh machine, 5–10 minutes if you already have Python and Git.

---

## Table of Contents

1. [Python 3.10+](#1-python-310)
2. [Git and GitHub](#2-git-and-github)
3. [Code Editor (VS Code or Cursor)](#3-code-editor)
4. [Python Virtual Environment](#4-python-virtual-environment)
5. [Required Python Packages](#5-required-python-packages)
6. [Google AI Studio Account and Free API Key](#6-google-ai-studio-account-and-free-api-key)
7. [Environment Variables and Secrets Management](#7-environment-variables-and-secrets-management)
8. [Verification Checklist](#8-verification-checklist)

---

## 1. Python 3.10+

### Check if you already have it

```bash
python --version
# or
python3 --version
```

If the output shows `Python 3.10.x` or higher, skip to Section 2.

### Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.12.x installer
3. Run the installer — **check "Add Python to PATH"** before clicking Install
4. Restart your terminal after installation

**macOS:**
```bash
# If you have Homebrew (recommended):
brew install python@3.12

# If you do not have Homebrew, install it first:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Then install Python:
brew install python@3.12
```

**Ubuntu / Debian Linux:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip -y
```

### Verify

```bash
python --version
# Expected: Python 3.12.x (or 3.10.x, 3.11.x — all acceptable)
```

---

## 2. Git and GitHub

### Install Git

**Windows:** Download and install from [git-scm.com/download/win](https://git-scm.com/download/win). Use all default settings.

**macOS:**
```bash
brew install git
# or, if you have Xcode Command Line Tools:
git --version  # this will prompt you to install if not present
```

**Ubuntu / Debian Linux:**
```bash
sudo apt install git -y
```

### Configure Git with your identity

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"
```

Use the same email address you use for your GitHub account.

### Set up SSH authentication for GitHub (recommended)

```bash
# Generate an SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter to accept the default location
# Set a passphrase (optional but recommended)

# Copy your public key to clipboard
# macOS:
cat ~/.ssh/id_ed25519.pub | pbcopy
# Linux:
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard
# Windows (PowerShell):
Get-Content ~/.ssh/id_ed25519.pub | Set-Clipboard
```

Then go to GitHub → Settings → SSH and GPG keys → New SSH key, and paste what you copied.

### Create your personal GitHub repository for this course

1. Go to [github.com/new](https://github.com/new)
2. Name it `cs-ai-2025-<your-student-id>` (e.g., `cs-ai-2025-s12345`)
3. Set it to **Private**
4. Add a README
5. Click **Create repository**

This is your personal repository where you will submit all individual homework assignments throughout the semester.

---

## 3. Code Editor

The course supports two primary editors. Both have excellent AI assistance built in.

### Option A: Cursor (Recommended for this course)

Cursor is an AI-first code editor built on VS Code. It includes Claude, GPT-4.1, and Gemini models directly in the editor for code completion, explanation, and generation.

1. Download from [cursor.com](https://cursor.com)
2. Install and open
3. Sign up for a free account (includes a free monthly quota for AI features)
4. Import your VS Code settings if you have them

### Option B: VS Code with GitHub Copilot

1. Download from [code.visualstudio.com](https://code.visualstudio.com)
2. Install the following extensions:
   - Python (Microsoft)
   - GitHub Copilot (free for verified students)
   - GitLens
   - Python Debugger

### Option C: Google Antigravity (Instructor's primary environment)

The course instructor uses Google Antigravity as the primary IDE. If you have access to it, it is an excellent choice for this course. Setup details will be provided separately.

### Recommended editor settings for Python AI development

Create a `.vscode/settings.json` in your project folder with these settings:

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "files.exclude": {
    "**/__pycache__": true,
    "**/.env": false
  }
}
```

---

## 4. Python Environment Setup

Always isolate your project's dependencies from your system Python. This course recommends `uv` — it is faster than pip, handles virtual environments automatically, and was highlighted in the Week 1 lecture slides.

### Option A: uv (Recommended)

```bash
# Install uv — Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install uv -- Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Restart your terminal, then verify:
uv --version

# Navigate to the Lab-1 directory and create your project
cd /path/to/AI-POWERED-SOFTWARE-DEV/course-pack/labs/Lab-1
uv init my-lab1 && cd my-lab1

# Add required packages (uv handles the venv automatically)
uv add google-genai python-dotenv

# Run scripts with uv (no manual activation needed)
uv run python examples/starter-code/01_hello_gemini.py
```

### Option B: pip + venv (Works everywhere, no extra install)

```bash
# Navigate to the Lab-1 directory
cd /path/to/AI-POWERED-SOFTWARE-DEV/course-pack/labs/Lab-1

# Create a virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Install packages
pip install google-genai python-dotenv
```

When your virtual environment is active, your terminal prompt will show `(venv)` at the beginning. You must activate it every time you open a new terminal session.

### Deactivate venv (when you are done)

```bash
deactivate
```

---

## 5. Required Python Packages

Install the packages for Lab 1 (if you used Option B above):

```bash
pip install google-genai python-dotenv
```

If you used `uv`, these were already added with `uv add` above.

Verify the installation:

```bash
python -c "import google.genai; import dotenv; print('All packages installed successfully')"
```

### What these packages do

**`google-genai`** — The official Google AI Python SDK. This is the library you use to call Gemini models. It handles authentication, request formatting, response parsing, token counting, and streaming.

**`python-dotenv`** — Loads environment variables from a `.env` file into your Python environment. This is how you keep your API key out of your source code while still being able to use it in your scripts.

### Optional but useful packages

```bash
pip install rich   # Beautiful terminal output with colors and formatting
pip install httpx  # HTTP client useful for understanding request/response cycles
```

---

## 6. Google AI Studio Account and Free API Key

### Create your account

1. Go to **[aistudio.google.com](https://aistudio.google.com)**
2. Sign in with your Google account (create one if needed — a Gmail account works perfectly)
3. Accept the terms of service

### Get your API key

1. In the left sidebar, click **"Get API key"**
2. Click **"Create API key"**
3. Select **"Create API key in new project"**
4. A key will be generated — it begins with `AIza` and is approximately 40 characters long
5. Click the copy button next to the key

**Important:** This key is shown to you now. If you close the window without saving it, you can always return to Google AI Studio and see your existing keys — you do not lose it.

### Understanding the free tier

| Limit | Value |
|-------|-------|
| Models available | Gemini 3 Flash, Gemini 3 Flash Thinking, and others |
| Requests per minute | 15 |
| Requests per day | 1,500 |
| Tokens per minute | 1,000,000 |
| Context window | 1,000,000 tokens |
| Cost | Free — no credit card required |

The free tier is sufficient for all of Lab 1 and Homework 1. You will not hit the daily limit doing normal coursework. The only limit you might approach is the 15 requests per minute — if you are running experiments in a loop, add a short sleep between calls.

See [`guides/gemini-setup-guide.md`](../guides/gemini-setup-guide.md) for more detail on managing free tier usage.

---

## 7. Environment Variables and Secrets Management

This section is non-negotiable. Every professional developer manages secrets this way. You are learning it on day one.

### The problem with hardcoded credentials

```python
# NEVER DO THIS
import google.genai as genai
client = genai.Client(api_key="AIzaSyAbCdEfGhIjKlMnOpQrSt")
```

If this code gets committed to Git and pushed to GitHub, your API key is public. Automated bots scan GitHub for exposed API keys and can use them within minutes. Google will likely detect this and revoke the key — but not before someone else has run up a bill on your account.

### The correct approach: `.env` files

**Create the `.env` file:**

```bash
# In your Lab-1 directory
touch .env   # creates an empty file (Mac/Linux)
# On Windows, just create a new file named .env in your editor
```

**Add your key to `.env`:**

```
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

No quotes. No spaces around the equals sign. One variable per line.

**Protect the file with `.gitignore`:**

```bash
# Check if .gitignore exists
ls -la | grep .gitignore

# Create or update .gitignore to exclude sensitive files
cat >> .gitignore << 'EOF'
# Environment variables — NEVER commit these
.env
.env.local
.env.*.local

# Virtual environment — always excluded
venv/
__pycache__/
*.pyc
*.pyo

# Editor files
.vscode/
.idea/
*.swp
EOF
```

**Load the key in your Python code:**

```python
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()  # reads .env file and adds variables to environment

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Check your .env file.")

client = genai.Client(api_key=api_key)
```

This pattern — `load_dotenv()` then `os.getenv()` — is the same pattern you will use throughout the entire course and in your professional work.

### Verify your `.gitignore` is working

```bash
git status
```

If `.env` appears in the output under "Untracked files" with a warning, your `.gitignore` is not working correctly. Double-check that `.env` is listed in the file (exactly, with no leading space).

If `.env` does not appear in `git status` output at all, your `.gitignore` is working correctly.

---

## 8. Verification Checklist

Before proceeding to the quickstart, confirm each item:

```
[ ] Python 3.10+ installed → python --version shows 3.10 or higher
[ ] Git installed and configured → git config --list shows your name and email
[ ] GitHub account created and SSH key added
[ ] Personal course repository created (private, named cs-ai-2025-<student-id>)
[ ] Code editor installed and working
[ ] Lab-1 directory cloned from course repository
[ ] Virtual environment created and activated → (venv) shows in terminal prompt
[ ] google-genai and python-dotenv installed → pip list shows both
[ ] Google AI Studio account created
[ ] Gemini API key copied from Google AI Studio
[ ] .env file created with GEMINI_API_KEY
[ ] .gitignore confirms .env is excluded from Git tracking
```

If all boxes are checked, go to [`quickstart.md`](../quickstart.md) and complete Step 4 (run your first API call).

---

## Getting Help

**During lab:** Raise your hand. The instructor and TAs circulate continuously.

**Specific error messages:** Read the full error message carefully. Python error messages are very descriptive. Copy the last line and paste it into the course forum or your preferred AI assistant.

**After lab:** Post in the course forum on GitHub or email zeshan.ahmad@kiu.edu.ge.

---

*Tools setup guide for CS-AI-2025 Lab 1, Spring 2026.*  
*If you find a step that is incorrect or unclear, post in the course forum so we can fix it.*

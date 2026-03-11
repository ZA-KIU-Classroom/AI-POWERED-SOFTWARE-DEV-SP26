# Lab 1 Quickstart

**Get from zero to a working AI application in 15 minutes.**

If you already have Python 3.10+ and Git installed, this is your starting point. If you need to install anything from scratch, start with [`tools-setup.md`](./tools-setup.md) and come back here.

> **Homework 1 reminder:** Due **before your Lab 2 session** — Friday 13 March 2026 (Group A: 09:00, Group B: 11:00). See [`homework/hw1-individual.md`](./homework/hw1-individual.md) for full requirements. Everything you set up in this quickstart is the foundation you will build on for HW1.

---

## Step 1: Get Your Free Gemini API Key (3 minutes)

1. Go to **[aistudio.google.com](https://aistudio.google.com)**
2. Sign in with your Google account
3. Click **"Get API key"** in the left sidebar
4. Click **"Create API key"**
5. Select **"Create API key in new project"**
6. Copy the key — it starts with `AIza`

Keep this tab open. You will need the key in Step 3.

For full details on the free tier limits and dashboard, see [`guides/gemini-setup-guide.md`](./guides/gemini-setup-guide.md).

---

## Step 2: Clone the Lab Repository and Create Your Environment (4 minutes)

Open your terminal (PowerShell on Windows, Terminal on Mac/Linux):

```bash
# Navigate to wherever you keep your coursework
cd ~/Documents   # or wherever you prefer

# Clone the course repository (if you have not already)
git clone https://github.com/ZA-KIU/AI-POWERED-SOFTWARE-DEV.git
cd AI-POWERED-SOFTWARE-DEV/course-pack/labs/Lab-1
```

**Recommended: use `uv`** (faster installs, recommended in this course — see slide 25)

```bash
# Install uv if you do not have it yet
# Mac / Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create a project folder and install packages
uv init my-lab1 && cd my-lab1
uv add google-genai python-dotenv
```

**Alternative: pip + venv** (works everywhere, no extra install required)

```bash
python -m venv venv

# Activate -- Mac/Linux:
source venv/bin/activate
# Activate -- Windows (PowerShell):
.\venv\Scripts\Activate.ps1

pip install google-genai python-dotenv
```

When setup is complete your terminal shows either your `uv` project name or `(venv)` at the prompt.

---

## Step 3: Store Your API Key Securely (2 minutes)

Never put your API key directly in your code. Create a `.env` file:

```bash
# In the Lab-1 directory, create a .env file
# On Mac/Linux:
echo "GEMINI_API_KEY=your_key_here" > .env

# On Windows (PowerShell):
Set-Content -Path .env -Value "GEMINI_API_KEY=your_key_here"
```

Replace `your_key_here` with the actual key you copied from Google AI Studio.

Then verify that `.gitignore` protects this file:

```bash
# Check if .env is in .gitignore
cat .gitignore | grep .env
```

If `.env` does not appear in the output, add it:

```bash
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
```

**This is not optional.** API keys committed to GitHub are detected by automated scanners within minutes, and the key gets invalidated. This has happened to students in every previous cohort.

---

## Step 4: Run Your First AI Call (3 minutes)

```bash
# Make sure you are in the Lab-1 directory with venv active
python examples/starter-code/01_hello_gemini.py
```

You should see output similar to:

```
Connecting to Gemini 3 Flash...
Prompt: Tell me one fascinating thing about language models in one sentence.
Response: Language models predict the next token based on patterns learned from
          hundreds of billions of words, yet this statistical process gives rise
          to what appears to be genuine reasoning and creativity.

Token usage:
  Input tokens:  15
  Output tokens: 38
  Total tokens:  53

Latency: 1.24 seconds
Estimated cost (free tier): $0.00
```

If you see a response like this, **you are done with the quickstart.** Proceed to Exercise 2 in the lab session.

---

## Step 5: Troubleshooting Common Issues

**`ModuleNotFoundError: No module named 'google'`**  
Your virtual environment is not active. Run `source venv/bin/activate` (Mac/Linux) or `.\venv\Scripts\Activate.ps1` (Windows) and try again.

**`google.api_core.exceptions.InvalidArgument: API key not valid`**  
Your API key in `.env` has a typo or extra space. Open `.env` in your editor and check it carefully. The key should be exactly as copied from Google AI Studio, with no quotes around it.

**`FileNotFoundError: .env not found`**  
Make sure you are running the script from the `Lab-1/` directory, not a parent folder. Run `pwd` to check your current location.

**`429 Resource Exhausted`**  
You have hit the free tier rate limit (15 requests per minute). Wait 60 seconds and try again. This is normal. See [`guides/gemini-setup-guide.md`](./guides/gemini-setup-guide.md) for strategies to avoid hitting this limit during development.

**`Permission denied: venv/Scripts/Activate.ps1`** (Windows only)  
Run PowerShell as administrator and execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`, then try activating again.

---

## What Comes Next in the Lab Session

| Exercise | File | Time |
|----------|------|------|
| Exercise 1 | `examples/starter-code/01_hello_gemini.py` | 20 min |
| Exercise 2 | `examples/starter-code/02_prompt_patterns.py` | 40 min |
| Exercise 3 | `examples/starter-code/03_token_counter.py` | 30 min |
| Homework walkthrough | `homework/hw1-individual.md` | 15 min |

---

*Quickstart for CS-AI-2025 Lab 1, Spring 2026. If this guide has an error, raise your hand immediately so we can fix it for Group B.*

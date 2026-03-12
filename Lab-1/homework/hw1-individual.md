# Homework 1 — Individual Assignment

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026  
**Type:** Individual (you must complete this alone)  
**Due:** Before your Lab 2 session — Friday 20 March 2026 (Group A: 09:00 | Group B: 11:00)  
**Weight:** 5 participation points  
**Submission:** Via course LMS — submit a link to your personal GitHub repository  
**Late policy:** 10% deducted per day. No submissions accepted after Sunday 15 March 2026 at 23:59.

---

## Overview

HW1 has one purpose: confirm that your development environment is fully working and that you can make real API calls to live language models. This is a setup and exploration assignment, not an application-building assignment. That comes in Week 2.

You will call at least two Gemini models, compare their responses, log your token usage, calculate costs, and write a short honest reflection on what surprised you.

---

## Your Six Tasks

### Task 1: Set Up Your Dev Environment

Your machine must have:

```
[ ] Python 3.10 or higher installed
[ ] uv (recommended) or pip + venv working
[ ] Git installed and configured (name + email)
[ ] python-dotenv and google-genai packages installed
[ ] .env file created with GEMINI_API_KEY
[ ] .env listed in .gitignore before any commit
```

See [`../quickstart.md`](../quickstart.md) and [`../tools-setup.md`](../tools-setup.md) for full setup instructions.

---

### Task 2: Create a GitHub Account and Fork the Course Repo

```
[ ] GitHub account active at github.com/your-username
[ ] Course repo forked: github.com/ZA-KIU/AI-POWERED-SOFTWARE-DEV
[ ] hw01/ folder created inside your fork (or a personal repo is fine)
```

---

### Task 3: Set Up Your Gemini API Key and Test It

```
[ ] Google AI Studio account created at aistudio.google.com
[ ] API key generated and stored in .env as GEMINI_API_KEY
[ ] .env is in .gitignore
[ ] You have successfully received at least one response from the API
```

---

### Task 4: Get a Response From at Least Two Different Models

Call **two different Gemini models** with the same or a similar prompt. Compare their responses. Suggested pair:

| Model | What it is |
|---|---|
| `gemini-3-flash-preview` | Fast, capable standard model — your primary |
| `gemini-3.1-flash-lite-preview` | Reasoning variant — shows chain-of-thought traces |

Ask each model the same question. Something that requires real thinking works well — a logic puzzle, a code problem, or an open-ended question about your capstone idea.

Your script(s) must:

```
[ ] Use python-dotenv to load GEMINI_API_KEY from .env (never hardcoded)
[ ] Call at least 2 different models
[ ] Print the response text from each model
[ ] Print the token counts from each call (input, output, total)
[ ] Print the latency in milliseconds for each call
[ ] Print the paid-tier cost equivalent for each call (even though you pay $0)
```

The starter code from Exercise 1 is your foundation — extend it or write fresh scripts, either is fine.

---

### Task 5: Log Token Counts and Calculate Cost

Create a simple markdown table in your `README.md` (or a separate `cost-analysis.md`) with one row per API call:

| Call | Model | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Cost (paid equiv.) |
|---|---|---|---|---|---|---|
| 1 | gemini-3-flash-preview | 38 | 64 | 102 | 1,240 | $0.000027 |
| 2 | gemini-3.1-flash-lite-preview | 38 | 218 | 256 | 4,820 | $0.000068 |

You do not need many calls — two is enough. The point is that you know how to read and record this data, not that you have a large sample.

---

### Task 6: Write a Reflection (5 sentences)

In your `README.md`, write exactly 5 sentences answering: **what surprised you about the responses?**

This is not a formal essay. It is a genuine observation. Consider: Did the reasoning model's output look different? Was one model faster? Did the token count match your expectation? Did a model say something unexpected?

---

## What to Submit

Push the following to your `/hw01` folder in your personal GitHub repo:

```
hw01/
  your_script.py          (or multiple .py files if you split them)
  README.md               (explains what you built, contains the cost table and reflection)
  .env.example            (shows the variable name but with a placeholder value, NOT your real key)
```

**Do not include your `.env` file.** Include `.env.example` instead:

```
# .env.example
GEMINI_API_KEY=your-key-here
```

Submit your GitHub repository link via the course LMS before your Lab 2 session begins.

---

## Grading (5 pts)

| Criterion | Points | What we check |
|---|---|---|
| Working script | 1.5 | Runs on a fresh clone with only a `.env` file added |
| Two models called | 1.0 | Both model strings appear in the code and both responses are printed |
| Token and cost table | 1.0 | Table present with real numbers (not copy-pasted from this spec) |
| Reflection | 1.0 | 5 sentences, specific and honest — not generic |
| Repo structure + README | 0.5 | hw01/ folder exists, README explains the work |

**Automatic deductions:**
- -1.0 if your real API key is committed to the repository in any file
- -0.5 if the script crashes on a fresh clone (missing imports, hardcoded paths, etc.)

---

## Frequently Asked Questions

**Can I use a different question for each model?**  
Yes, but using the same prompt for both makes the comparison more meaningful.

**My API key keeps getting rejected. What do I do?**  
Check that the key starts with `AIza`, that it is in `.env` as `GEMINI_API_KEY=AIza...` (no quotes, no spaces), and that you are calling `load_dotenv()` before reading `os.getenv()`.

**What if gemini-3.1-flash-lite-preview is not available in my region?**  
Try `gemini-3-flash-preview` as your second model. If that also fails, use `gemini-3-flash-preview` — it is older but universally available on the free tier.

**Do I need to implement prompt patterns in HW1?**  
No. That comes in Week 2. For HW1, a simple user message is enough. The focus is your environment and your first real API calls.

**I already built more than this. Is that okay?**  
Yes — you will not be penalised for going further. But do not let scope creep stop you from submitting. Two working model calls, a cost table, and a reflection is a complete submission.

---

*Homework 1 — CS-AI-2025 Spring 2026*

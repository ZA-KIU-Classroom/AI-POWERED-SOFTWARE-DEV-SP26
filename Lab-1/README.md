# Lab 1: Environment Setup and Your First AI Application

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026  
**Week:** 1 of 15  
**Date:** Friday, 6 March 2026  
**Group A:** 09:00 – 11:00 | **Group B:** 11:00 – 13:00  
**Location:** Computer Science Lab, Kutaisi International University  
**Instructor:** Professor Zeshan Ahmad — zeshan.ahmad@kiu.edu.ge

---

## Overview

Welcome to your first lab in CS-AI-2025. Yesterday in lecture you saw the big picture: why this is the most important moment in history to be learning to build with AI, what the agent loop looks like, and how the entire course arc flows. Today you put your hands on the keyboard and make something run.

By the end of this two-hour session, every student in the room will have a fully working AI development environment and will have made their first call to a live language model. That is the only goal for today. Everything else — teams, proposals, capstone projects — comes in subsequent weeks. Right now: get set up, make it work, understand what you built.

Lab 1 uses the **Google Gemini free tier** accessed through Google AI Studio. This means you can complete everything today, and complete Homework 1, with zero cost to you. Starting in Lab 2, the course will transition to OpenRouter with provisioned organizational credits. For now: free tier, no friction, maximum focus on the fundamentals.

---

## Learning Objectives

By the end of Lab 1 you will be able to:

1. Set up a Python development environment configured for AI API work
2. Obtain and securely store a Gemini API key from Google AI Studio
3. Make your first authenticated API call to a frontier language model
4. Implement and compare at least three distinct prompt engineering patterns
5. Measure and record token usage, latency, and estimated cost for each call
6. Understand the difference between standard and reasoning model behaviour
7. Apply secrets management best practices from day one (`.env` files, `.gitignore`)

---

## What You Will Build Today

During the 2-hour lab session you will build three things in sequence:

**Exercise 1 — Hello AI (20 minutes)**  
Run the starter script that makes your first Gemini API call. Verify authentication. See a response. Celebrate.

**Exercise 2 — Prompt Pattern Explorer (40 minutes)**  
Modify and extend the prompt patterns script to experiment with zero-shot, few-shot, chain-of-thought, and system-prompt patterns on a topic of your choosing. Log every call.

**Exercise 3 — Token and Cost Tracker (30 minutes)**  
Run the token counter script against your prompt log. Fill in the cost tracker template. Understand what you actually spent (likely: $0.00 on free tier, but you will know *why*).

**Remaining Time — Homework Briefing and Q&A (30 minutes)**  
The last half hour is dedicated to walking through Homework 1, answering setup questions, and ensuring everyone is ready to work independently before next Thursday.

---

## Homework 1: Individual — Due Before Lab 2 (Friday 13 March 2026)

> **This is your first individual homework assignment.** It is worth **5 participation points**. Submit before your Lab 2 session (Group A: 09:00, Group B: 11:00). This is a setup and exploration assignment — two model calls, a cost table, and a short reflection.

Full details, requirements, and the submission checklist are in [`homework/hw1-individual.md`](./homework/hw1-individual.md).

**Summary of what you will submit (push to `/hw01` in your personal repo):**
- Python script(s) that call at least two Gemini models
- `README.md` with a cost analysis table and a 5-sentence reflection
- `.env.example` showing the variable name (never your real key)
- Your GitHub repository link submitted via the course LMS

**Late policy:** 10% deducted per day. No submissions accepted after Sunday 15 March at 23:59.

---

## Lab Schedule (Both Groups)

| Time | Activity | Duration |
|------|----------|----------|
| :00 | Arrival, setup checks, troubleshooting queue | 5 min |
| :05 | Lab intro: what we are building and why | 10 min |
| :15 | Exercise 1: Hello AI — first API call | 20 min |
| :35 | Exercise 2: Prompt Pattern Explorer | 40 min |
| :55 | Short break, stretch, compare results with a neighbour | 5 min |
| :60 | Exercise 3: Token and Cost Tracker | 30 min |
| :90 | Homework 1 walkthrough | 15 min |
| :105 | Open Q&A, troubleshooting, wrap-up | 15 min |
| :120 | End of lab |  |

*Group A runs 09:00 – 11:00. Group B runs 11:00 – 13:00.*

---

## Prerequisites

Before arriving at the lab (or in the first 10 minutes if you could not do it beforehand), you need:

- Python 3.10 or higher installed on your machine
- A Google account (Gmail is fine)
- VS Code, Cursor, or any code editor you are comfortable with
- Git installed and configured with your name and email
- A GitHub account

If you are missing any of these, start with [`tools-setup.md`](./tools-setup.md) immediately. The TAs will also be running a setup queue for the first 10 minutes of each group's session.

---

## How to Navigate This Lab

```
README.md  ← You are here. Start here every week.
    │
    ├── quickstart.md          ← Get running in 15 minutes (start here if set up)
    ├── tools-setup.md         ← Full environment setup guide (start here if not set up)
    │
    ├── guides/
    │   ├── gemini-setup-guide.md        ← Getting your free API key
    │   ├── prompt-engineering-101.md    ← The four patterns you need today
    │   └── token-and-cost-guide.md      ← Understanding tokens and pricing
    │
    ├── templates/
    │   ├── prompt-log-template.md       ← Copy this, fill it in during lab
    │   ├── cost-tracker-template.md     ← Copy this, fill it in during lab
    │   └── reflection-template.md       ← Use this for your HW1 submission
    │
    ├── examples/
    │   ├── example-prompt-log.md        ← Completed example for reference
    │   └── starter-code/
    │       ├── 01_hello_gemini.py       ← Exercise 1
    │       ├── 02_prompt_patterns.py    ← Exercise 2
    │       └── 03_token_counter.py      ← Exercise 3
    │
    ├── homework/
    │   └── hw1-individual.md            ← Full homework requirements
    │
    └── grading-rubric.md               ← How HW1 is graded
```

---

## The Models You Will Use Today

In Lab 1 you will work with the **Gemini 3 series free-tier models** via the Google AI Studio free tier. You will call two different models — one for your main exercises and one for your HW1 comparison.

| Property | Primary Model | Second Model (HW1) |
|----------|--------------|-------------------|
| Model ID | `gemini-3-flash-preview` | `gemini-3.1-flash-lite-preview` |
| Series | Gemini 3 Flash | Gemini 3.1 Flash-Lite |
| Access | Google AI Studio free tier | Google AI Studio free tier |
| Context window | 1,000,000 tokens | 1,000,000 tokens |
| Free tier limit | 10 requests per minute, 1,000 per day | 10 requests per minute, 1,000 per day |
| Input pricing (paid tier) | $0.10 per 1M tokens | $0.25 per 1M tokens |
| Output pricing (paid tier) | $0.40 per 1M tokens | $1.50 per 1M tokens |

The current frontier models as of March 2026 are **Gemini 3.1** (Google), **GPT-5.2** (OpenAI), and **Claude Opus 4.6** (Anthropic). The free-tier models you use today are in the same Gemini 3 generation — ideal for learning and prototyping without spending anything.

Starting in Lab 2, you will gain access to OpenRouter organizational credits that allow you to call frontier models including Gemini 3.1 Pro, Claude Opus 4.6, and GPT-5.2. This week, the Gemini 3 free tier is your tool. Learn it well.

---

## Key Concepts From Lecture to Reinforce Today

These are the concepts from Thursday's lecture that today's exercises will make concrete:

**The Agent Loop** — Perceive → Reason → Act → Observe. Every API call you make today is a single cycle through this loop. The prompt is the input to "Perceive". The model's reasoning is "Reason". The response is "Act". Reading and logging the output is "Observe".

**Prompt Patterns** — The way you structure input to the model dramatically changes the quality and type of output you receive. Zero-shot, few-shot, chain-of-thought, and system-prompt patterns are not tricks — they are the fundamental vocabulary of AI application development.

**Token Economics** — Every character you send and receive costs tokens. Tokens cost money and time. Understanding this from your very first call shapes how you think about every application you build in this course.

**Secrets Management** — Your API key is a credential. It should never appear in your code or your Git history. The `.env` pattern you set up today is the same pattern you will use in production systems.

---

## Common Mistakes to Avoid Today

**Do not hardcode your API key.** If you type `api_key = "AIza..."` in your Python file, that key will end up in your Git history and potentially on GitHub. Use `.env` files and `python-dotenv`. This is covered in the quickstart.

**Do not skip the token counter.** It feels tedious. Do it anyway. Students who skip cost tracking in Week 1 are consistently shocked by their bills in Weeks 5 through 8 when they start building larger systems.

**Do not share your API key.** Free tier keys are personal. Each person in the class gets their own Google AI Studio account and their own key.

**Do not panic if the API returns an error.** Error handling is part of the craft. Read the error message, look it up in the guide, and ask for help if you are stuck for more than 5 minutes.

---

## Resources

**In This Lab Folder:**
- [Quickstart](./quickstart.md) — fastest path to a working environment
- [Tools Setup](./tools-setup.md) — full setup guide
- [Gemini Setup Guide](./guides/gemini-setup-guide.md) — API key and configuration
- [Prompt Engineering 101](./guides/prompt-engineering-101.md) — the four patterns
- [Token and Cost Guide](./guides/token-and-cost-guide.md) — understanding token economics
- [Homework 1](./homework/hw1-individual.md) — full homework requirements
- [Grading Rubric](./grading-rubric.md) — how this is graded

**External Documentation:**
- [Google AI Studio](https://aistudio.google.com) — your free tier dashboard
- [Gemini API Python Quickstart](https://ai.google.dev/gemini-api/docs/quickstart?lang=python)
- [google-genai SDK Reference](https://googleapis.github.io/python-genai/)
- [Course GitHub Repository](https://github.com/ZA-KIU/AI-POWERED-SOFTWARE-DEV)

**Questions?**
- During lab: raise your hand or approach the instructor / TA
- After lab: post in the course forum (preferred — others benefit from your question)
- Email: zeshan.ahmad@kiu.edu.ge — expect a response within 48 hours on weekdays
- Office hours: email to schedule a Google Meet appointment

---

## Looking Ahead: What Lab 2 Will Expect

Lab 2 (Friday 13 March) will assume that every student has a working Python environment and a Gemini API key. It will also introduce OpenRouter with your organizational credits. Lab 2 is where teams form and the capstone project begins — so arrive having completed Homework 1 and with ideas about what kind of AI application you want to spend the semester building.

---

*Lab materials for CS-AI-2025 Spring 2026. Maintained at [github.com/ZA-KIU/AI-POWERED-SOFTWARE-DEV](https://github.com/ZA-KIU/AI-POWERED-SOFTWARE-DEV).*  
*Last updated: March 2026.*

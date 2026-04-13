# Lab 5: Capstone Prototype Sprint

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026
**Lab Date:** Friday 10 April 2026
**Group A:** 09:00 – 11:00 | **Group B:** 11:00 – 13:00
**Location:** Computer Lab / Bring Your Own Laptop

---

## What This Lab Is

Lab 5 is the first time your team writes production-bound code for your capstone. Everything before this was learning, exploring, and planning. Today you build.

By the end of this session, your team must have:

1. A completed **Design Decisions document** that closes the loop on your Design Review feedback
2. A **working AI-powered endpoint** — one route, real input, real model output, no mocks
3. A **cost log** capturing every API call made during the sprint
4. Your work **committed, tagged, and pushed** to your team repo

This is not a polish session. Working and ugly is better than pretty and fake.

---

## Before You Arrive

Both of the following must be done before lab starts. Do not use lab time for these.

- [ ] HW2 Individual Audio submitted via your personal repo before Thursday 23:59
- [ ] Your team repo cloned and environment running on at least one laptop
- [ ] Your Design Review feedback notes open and ready (email or LMS)
- [ ] OpenRouter key set in your `.env` file and verified working

If your OpenRouter key has stopped working, email `zeshan.ahmad@kiu.edu.ge` before Friday morning.

---

## Lab Structure

| Time | Activity | Duration |
|------|----------|----------|
| :00 | Arrival, setup checks, blockers queue | 5 min |
| :05 | Lab intro and objectives | 5 min |
| :10 | **Part 1:** Design Decisions document | 25 min |
| :35 | **Part 2:** Prototype sprint — first working endpoint | 70 min |
| :45 | Mid-sprint check-in (instructor circulates) | within Part 2 |
| :105 | **Part 3:** Commit, tag, push, and wrap-up form | 15 min |
| :120 | End of lab | |

*Times are from session start — Group A 09:00, Group B 11:00.*

---

## Part 1: Design Decisions Document (25 min)

Open `templates/design-decisions.md`. Fill it in as a team. This is written work — no verbal presentation required.

The document asks three things:

1. What are you changing based on Design Review feedback?
2. What are you keeping and why?
3. What is your first prototype milestone — the single most important feature you will attempt to build today?

This document goes into your team repo at `docs/design-decisions-lab5.md`. It is reviewed by the instructor as part of your capstone progress record.

---

## Part 2: Prototype Sprint — Your First Working Endpoint (70 min)

### The Sprint Goal

By 17:45 (Group A) / 12:45 (Group B), your team must have one working endpoint that:

- Accepts real input from a user or another part of your system
- Calls an AI model via OpenRouter (or Google AI Studio as fallback)
- Returns a real, non-mocked AI-generated response
- Logs the model name, input token count, output token count, and latency for the call

That is it. One endpoint. Working. Logged.

### Choosing Your Stack

Pick the scaffold that matches your Design Review architecture. Do not switch stacks mid-project.

| If your team chose... | Use this scaffold |
|---|---|
| Python backend (FastAPI, Flask) | `examples/fastapi-scaffold/` |
| JavaScript / TypeScript (Next.js, Node) | `examples/nextjs-scaffold/` |
| Something else | Read `guides/custom-stack-guide.md` |

### Using Your AI Coding Assistant

This lab is explicitly designed for agentic development. Use Cursor, VS Code with Continue, or Claude Code to help you write code. The expectation is that you are directing the agent, reviewing its output, and understanding every line it produces — not pasting output blindly.

See `guides/agentic-dev-guide.md` for prompting strategies that work well for this sprint.

### The Cost Log

Every API call your prototype makes must be captured in the cost log. Use `templates/cost-log-template.md` as your running log during the sprint. This data feeds your Week 11 Safety and Evaluation Audit. Do not reconstruct it after the fact.

### Team Health Check

At any point during the sprint, each team member should individually complete the anonymous team health check form at `templates/team-health-check.md`. Takes under three minutes. Submit individually via the course LMS link posted in class.

---

## Part 3: Commit, Tag, Push, and Wrap-up (15 min)

Before lab ends, every team must:

```bash
# 1. Stage all changes
git add .

# 2. Commit with a clear message
git commit -m "lab5: first prototype endpoint + design decisions doc"

# 3. Tag this checkpoint
git tag lab5-checkpoint

# 4. Push everything including the tag
git push origin main --tags
```

Then fill in `templates/lab5-wrapup.md` and submit it individually via the course LMS. It asks three questions and takes five minutes. It is how the instructor knows what each team actually shipped today.

---

## File Map

```
Lab-5/
├── README.md                        ← You are here
├── QUICKSTART.md                    ← Get your environment ready in 10 minutes
├── GRADING-RUBRIC.md                ← How this lab feeds your capstone grade
├── INSTRUCTOR-GUIDE.md              ← For the instructor and TAs
│
├── templates/
│   ├── design-decisions.md          ← Part 1: fill this in as a team
│   ├── cost-log-template.md         ← Track every API call during the sprint
│   ├── team-health-check.md         ← Individual anonymous form
│   └── lab5-wrapup.md               ← Submit individually at end of lab
│
├── guides/
│   ├── openrouter-setup-guide.md    ← Verify your key and test a call
│   ├── agentic-dev-guide.md         ← How to use Cursor/Claude Code effectively
│   ├── cost-tracking-guide.md       ← Logging pattern for every framework
│   └── custom-stack-guide.md        ← If you are not on FastAPI or Next.js
│
└── examples/
    ├── fastapi-scaffold/            ← Python FastAPI starter
    │   ├── main.py
    │   ├── routers/ai_router.py
    │   ├── services/llm_service.py
    │   ├── models/request_models.py
    │   ├── .env.example
    │   ├── pyproject.toml
    │   └── README.md
    └── nextjs-scaffold/             ← Next.js / TypeScript starter
        ├── app/api/ai/route.ts
        ├── lib/llm-service.ts
        ├── lib/cost-logger.ts
        ├── types/ai-types.ts
        ├── .env.example
        ├── package.json
        └── README.md
```

---

## What a Successful Lab 5 Looks Like

At the end of lab, an instructor should be able to:

1. Clone your team repo
2. Add a `.env` file with your OpenRouter key
3. Run one command to start the app
4. Send one HTTP request (or interact with one UI element) that calls an AI model
5. See the response plus a cost log entry in the terminal or a log file

If that is true, you succeeded today.

---

## Resources

**In This Lab Folder:**
- `QUICKSTART.md` — fast environment check
- `guides/openrouter-setup-guide.md` — key verification and test call
- `guides/agentic-dev-guide.md` — Cursor and Claude Code prompting strategies

**External:**
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Google AI Studio](https://aistudio.google.com)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Course GitHub](https://github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26)

**Questions:**
- During lab: raise your hand or use the help queue on the board
- After lab: post in the course forum (others benefit from your question)
- Email: `zeshan.ahmad@kiu.edu.ge` — response within 48 hours on weekdays
- Office hours: book via email for a Google Meet slot

---

*Lab 5 materials for CS-AI-2025 Spring 2026.*
*Maintained at [github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26](https://github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26)*

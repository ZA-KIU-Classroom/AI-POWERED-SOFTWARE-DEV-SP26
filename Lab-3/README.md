# Lab 3: Design Review Sprint

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026
**Week:** 3 of 15
**Date:** Friday, 27 March 2026
**Group A:** 09:00 – 11:00 | **Group B:** 11:00 – 13:00
**Location:** Computer Science Lab, Kutaisi International University
**Instructor:** Professor Zeshan Ahmad — zeshan.ahmad@kiu.edu.ge

---

## What Lab 3 Is

Lab 3 is entirely dedicated to building your Design Review. This is the first major capstone checkpoint and is worth **10 points**.

You already have the raw material from Labs 1 and 2 — your individual HW1 work, your team's six-section proposal draft, your scaffold, and your working vision call. Lab 3 takes that material and lifts it into a submission-ready Design Review by filling the gaps: measurable success criteria, a real architecture diagram with data flows, safety threats, fallback UX design, and data governance. You also sign and commit your team contract today.

The entire two hours is team work. There are no individual technical exercises in Lab 3 — those move to Lab 4 where you cover image generation and audio together.

**Design Review due: Thursday 2 April 2026 at 23:59 Georgia Time.**
Submission is your team repo (see required tree below) plus the Google Form link shared in lab and on Teams. There is no presentation.

---

## Status Check Before You Start

Resolve anything missing in the first 10 minutes. Raise your hand immediately — do not skip ahead.

### From Lab 1 (individual — in your personal fork of the course repo)
- [ ] `hw1/` submitted — script calling two Gemini models, README with cost table and reflection, `.env.example`
- [ ] `templates/reflection-template.md` completed

### From Lab 2 (team — in your team project repo)
- [ ] Team project repo exists under `github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26`
- [ ] All team members have push access
- [ ] `frontend/` scaffold committed from Builder Sprint (Bolt / Lovable / v0 export)
- [ ] `backend/` folder exists with at least a placeholder
- [ ] Working vision call committed (image input + AI response)
- [ ] Six-section proposal draft completed — all 6 sections at least started
- [ ] Team roles assigned in writing
- [ ] OpenRouter API key confirmed working

---

## Required Team Repo Tree at Submission

This is the structure you began setting up in Lab 2. Today you are adding `TEAM-CONTRACT.md` and filling in `docs/design-review/`. The grader navigates this tree directly.

```
[your-project-name]/
├── README.md                          ← Project overview — update this today
├── TEAM-CONTRACT.md                   ← New today — signed by all members
├── .gitignore                         ← Covers .env, node_modules, __pycache__, venv/
├── .env.example                       ← Variable names with placeholder values, no real keys
├── AGENTS.md                          ← Optional but encouraged
│
├── frontend/                          ← To be added
│   └── [scaffold files]
│
├── backend/                           ← Or api/, server/
│   └── [backend files]
│
├── docs/
│   └── design-review/                 ← Create this folder today
│       ├── DESIGN-REVIEW.md           ← Main submission document, no [fill in] remaining
│       └── architecture-diagram.png   ← Committed diagram — hand-drawn photo is fine
│
└── tests/                             ← Empty for now
```

**Graders will check:**
- `TEAM-CONTRACT.md` in repo root with all member names typed in Signatures
- `docs/design-review/DESIGN-REVIEW.md` has no `[fill in]` remaining
- `docs/design-review/architecture-diagram.png` exists and is readable
- `.env` is NOT committed — confirm your `.gitignore` covers it
- `frontend/` scaffold from Lab 2 is present

---

## Lab 3 Agenda: 120 Minutes

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Status check, fix blockers, triage Design Review gaps |
| 0:10 – 0:30 | Success criteria — sharpen from your Lab 2 proposal |
| 0:30 – 0:55 | Architecture diagram and data flow |
| 0:55 – 1:20 | Safety threats, fallback UX, data governance |
| 1:20 – 1:40 | Team contract — sign and commit as `TEAM-CONTRACT.md` |
| 1:40 – 1:55 | Create `docs/design-review/`, commit everything, verify repo tree |
| 1:55 – 2:00 | Wrap-up |

---

## What You Are Building Today

| Design Review section | Source | Status entering Lab 3 | Action today |
|---|---|---|---|
| Problem statement and users | Lab 2 proposal section 1 | Draft exists | Sharpen to one precise sentence |
| Proposed solution and features | Lab 2 proposal section 2 | Draft exists | Confirm 3–5 features, name the AI differentiator |
| Measurable success criteria | Not in Labs 1 or 2 | Missing | Write at least 2 criteria with numbers |
| Team roles | Lab 2 proposal section 5 | Draft exists | Carry into Design Review and Team Contract |
| IRB-light checklist | Lab 2 proposal section 6 | Draft exists | Review and confirm |
| Architecture diagram | Lab 2 proposal section 3 — prose only | No visual yet | Draw and commit to `docs/design-review/` |
| Prompt and data flow | Not in Labs 1 or 2 | Missing | Trace one full user action |
| Safety threats | Not in Labs 1 or 2 | Missing | Name at least 3 with mitigations |
| Fallback UX | Not in Labs 1 or 2 | Missing | Describe what the user sees |
| Data governance | Not in Labs 1 or 2 | Missing | Answer 6 questions |
| Team contract | Syllabus: due Week 3 | Missing | Sign and commit today |

---

## Guides, Templates, and Examples

Everything you need is in the `design-review/` folder of the Lab 3 course materials. Open the relevant guide before filling in each section.

```
Lab-3/design-review/
├── DESIGN-REVIEW.md                   ← The submission document — copy to your repo
├── GRADING-RUBRIC.md                  ← How each section is scored
│
├── guides/
│   ├── success-criteria-guide.md      ← How to write measurable criteria
│   ├── architecture-guide.md          ← What the diagram must include
│   ├── data-flow-guide.md             ← How to trace a prompt-to-output flow
│   ├── safety-threats-guide.md        ← The six threats with explanations
│   ├── fallback-ux-guide.md           ← Fallback as UX, not error handling
│   └── data-governance-guide.md       ← Six questions and why they matter
│
├── templates/
│   ├── team-contract-template.md      ← Fill in, commit as TEAM-CONTRACT.md in repo root
│   ├── problem-statement-template.md  ← Sharpen your Lab 2 problem statement
│   ├── architecture-template.md       ← Checklist before committing your diagram
│   ├── data-flow-template.md          ← Step-by-step trace format
│   ├── safety-threats-template.md     ← Threat table
│   ├── fallback-ux-template.md        ← User-facing description template
│   └── data-governance-template.md    ← Six-question form
│
└── examples/
    ├── success-criteria-example.md    ← Weak vs strong, with numbers
    ├── architecture-example.md        ← Worked architecture description
    ├── data-flow-example.md           ← Complete trace for a sample project
    ├── safety-threats-example.md      ← Filled threat table
    └── fallback-ux-example.md         ← Before and after
```

---

## Submission

**Due:** Thursday 2 April 2026 at 23:59 Georgia Time

**Two steps — both required:**
1. Push your team repo matching the tree above with `docs/design-review/DESIGN-REVIEW.md` complete
2. Complete the Google Form — link shared in lab today and posted on Teams

One team member submits the Google Form on behalf of the team.

---

*Lab 3 for CS-AI-2025 Spring 2026.*
*Design Review due: Thursday 2 April 2026 at 23:59. Submission: repo + Google Form.*

# Lab 3 Grading Rubric

**Course:** CS-AI-2026 Spring 2026 | **Lab:** 3 | **Date:** Friday 27 March 2026

---

## Lab 3 Participation

Recorded by the TA based on presence and active contribution. Checked at the end of the session.

| Check | Pass condition |
|---|---|
| Team present and working together | All members present, actively writing or coding |
| `TEAM-CONTRACT.md` committed to team repo root | File exists with all member names in Signatures section |
| `docs/design-review/DESIGN-REVIEW.md` exists | File committed and sections in progress |
| At least one architecture diagram committed | `docs/design-review/architecture-diagram.png` or equivalent exists |
| `docs/design-review/` folder created in correct location | Inside `docs/`, not at repo root |

---

## Design Review: 10 Points

**Due:** Thursday 2 April 2026 at 23:59 Georgia Time
**Submission:** Team repo + Google Form (link shared in lab and on Teams)

### Required Team Repo Tree

The grader navigates this tree directly. Files in the wrong location or with wrong names score zero for that section.

```
[your-project-name]/
├── README.md
├── TEAM-CONTRACT.md                   ← Repo root — not inside docs/
├── .gitignore                         ← .env must be excluded
├── .env.example
├── AGENTS.md                          ← Optional
│
├── frontend/                          ← Scaffolding added at a later date
│   └── [scaffold files]
│
├── backend/
│   └── [backend files]
│
├── docs/
│   └── design-review/                 ← Correct location for Design Review files
│       ├── DESIGN-REVIEW.md           ← No [fill in] remaining
│       └── architecture-diagram.png   ← Readable visual
│
└── tests/
```

**Common mistakes that cost marks:**
- `DESIGN-REVIEW.md` placed at repo root instead of inside `docs/design-review/`
- `TEAM-CONTRACT.md` placed inside `docs/` instead of repo root
- Architecture diagram not committed (description in prose does not count)
- `.env` file committed (automatic deduction)

---

### Rubric Breakdown (10 points total)

#### Criterion 1 — Clarity and Scope (2 points)

Sections 1, 2, and 3 of DESIGN-REVIEW.md.

| Score | What it looks like |
|---|---|
| **2.0** | Problem names a specific user, specific pain, specific consequence. At least 2 success criteria have target numbers and measurement methods. |
| **1.5** | Problem is specific but success criteria lack numbers, or one criterion is qualitative. |
| **1.0** | Problem is generic ("people have trouble with X"). Success criteria are qualitative only. |
| **0.5** | Problem statement is vague. No success criteria present. |
| **0** | Section missing or entirely placeholder text. |

**The line between 1.0 and 2.0:** A number. "Our extraction will be accurate" is 1.0. "Our extraction achieves greater than 85% field accuracy on a 20-item test set" is 2.0.

---

#### Criterion 2 — Technical Depth (3 points)

Sections 4 and 5 of DESIGN-REVIEW.md.

| Score | What it looks like |
|---|---|
| **3.0** | `architecture-diagram.png` committed and shows all five required elements (frontend, backend, named AI model, storage, arrows). Data flow traces a complete user action through every layer. Technology stack table complete. |
| **2.0** | Diagram exists but is missing one or two elements. Data flow present but incomplete. |
| **1.0** | Architecture described in prose only — no diagram committed. Data flow absent. |
| **0** | No architecture section. No diagram. |

**The five required diagram elements:**
1. Frontend (label what it actually is — browser, mobile app, Gradio UI, CLI)
2. Backend (label what it actually is — FastAPI, Flask, Next.js)
3. AI model (name it specifically — Gemini 3 Flash, DALL-E 3, not just "AI")
4. Storage (name it — Postgres, SQLite, FAISS, Supabase)
5. Arrows showing data direction between all connected components

A hand-drawn photo committed as `.png` earns the diagram point. Prose does not.

---

#### Criterion 3 — Reliability and Safety (3 points)

Sections 7 and 8 of DESIGN-REVIEW.md.

| Score | What it looks like |
|---|---|
| **3.0** | Three or more threats named with specific one-sentence mitigations. Fallback UX describes what the user sees (not error handling code). Data governance answers all six questions. |
| **2.0** | Threats present but mitigations vague. Fallback UX exists but framed as code logic. Data governance has at least 3 answers. |
| **1.0** | One or two threats mentioned. No fallback UX. Data governance fewer than 3 answers. |
| **0** | Section missing or entirely placeholder text. |

**The line between 2.0 and 3.0 on fallback UX:**
- 2.0: "We will catch errors and show a message."
- 3.0: "The user sees the fields highlighted in amber with 'Please check these values'. A manual entry option appears below. The word 'error' is never shown."

---

#### Criterion 4 — UX and Communication (2 points)

Overall document quality, team contract, and repo structure.

| Score | What it looks like |
|---|---|
| **2.0** | `DESIGN-REVIEW.md` complete — no placeholder text. `TEAM-CONTRACT.md` in repo root with all names. Repo tree matches required structure. `README.md` updated. |
| **1.5** | Document mostly complete with minor gaps. Contract exists. |
| **1.0** | Multiple sections have placeholder text. Contract missing or unsigned. |
| **0.5** | Document fragmentary. Repo structure not recognisable. |
| **0** | Not submitted or Google Form not completed. |

---

### Late Policy

| Hours late | Maximum score |
|---|---|
| On time | 10 |
| Up to 24 hours | 9 |
| 24 – 48 hours | 8 |
| 48 – 72 hours | 7 |
| Over 72 hours | Contact instructor before submitting |

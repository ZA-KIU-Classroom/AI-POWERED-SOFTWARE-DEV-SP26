# Lab 7: Agents, Orchestration, Resilience, and Safety

**Course:** CS-AI-2025, Building AI-Powered Applications, Spring 2026  
**Lab Date:** Friday 24 April 2026  
**Group A:** 09:00 to 11:00, **Group B:** 11:00 to 13:00  
**Location:** Computer Lab / Bring Your Own Laptop

---

## What This Lab Is

Lab 6 gave your capstone a live response loop. Lab 7 turns that loop into an agent architecture.

By the end of this session, your team must have:

1. Chosen and documented an **agent pattern** for the capstone, orchestrator/specialist, supervisor/worker, peer/pipeline, or a justified single-agent design
2. Defined an explicit **AgentState** structure with named and typed fields
3. Added **timeouts** to every LLM call and **exponential backoff retries** to every external AI call
4. Added a **human approval checkpoint** for any high-stakes or irreversible action, or documented why your system has no such action
5. Extended the **episode log** so it records errors, retry counts, timeout values, and success or failure, not only happy-path calls
6. Built a small **two-node orchestration proof** using the LangGraph starter or an equivalent raw-Python orchestration flow
7. Committed all changes and tagged the repo with `lab7-agent-architecture-checkpoint`

This lab does **not** create a separate grading checkpoint. The work you do here feeds directly into the **Week 11 Safety and Evaluation Audit** and improves your **Week 15 Repository Review**.

---

## Before You Arrive

All of the following must be done before lab starts.

- [ ] Your Lab 6 streaming endpoint still works locally
- [ ] Your Lab 6 session memory still works across at least 5 turns
- [ ] Your team has already discussed which agent pattern best fits the capstone
- [ ] Your episode log already captures the core fields from prior labs
- [ ] Python 3.10+ is installed on at least one laptop in the team
- [ ] Node 18+ is installed if your capstone uses Next.js
- [ ] You have pulled the latest version of your team repo on every machine you plan to use
- [ ] You have read `QUICKSTART.md`

Do not use Lab 7 time to repair a broken Lab 6 baseline.

---

## Lab Structure

| Time | Activity | Duration |
|---|---|---|
| :00 | Arrival, baseline checks, blockers queue | 5 min |
| :05 | Lab intro and objectives | 5 min |
| :10 | **Part 1:** Architecture sprint, choose pattern, define state, add resilience and safety plan | 50 min |
| :60 | **Part 2:** LangGraph mini-build, two nodes plus checkpoint routing | 45 min |
| :105 | **Part 3:** Capstone integration, README update, commit, tag, push | 15 min |
| :120 | End of lab | |

---

## Part 1: Architecture Sprint (50 min)

### The Goal

Move from “we have a chatbot” to “we have an architecture.”

By the 50-minute mark, your team must have made the main design decisions that govern how your agent behaves under load, failure, and risk.

### The Decisions You Must Make

#### 1. Choose a pattern

Pick one of the following:

- **Orchestrator / Specialist**  
  One main agent breaks the task into smaller parts and delegates them to focused sub-agents.

- **Supervisor / Worker**  
  One controller monitors repeated or parallel worker tasks and retries or reroutes failed work.

- **Peer / Pipeline**  
  Agents pass work in sequence. Each one transforms the output before handing it forward.

- **Single agent, justified**  
  This is allowed. If you stay single-agent, state clearly why a second agent would add complexity without enough value.

Read `guides/agent-patterns-guide.md` before deciding.

#### 2. Define `AgentState`

Your architecture must define a shared state object or dataclass. It must include only fields your system truly needs.

At minimum, include:

- `session_id`
- `user_request`
- `messages`
- `current_step`
- `approval_required`
- `approved`
- `retry_count`
- `timeout_ms`
- `last_error`
- one domain field specific to your project

Use `templates/agentstate-template.md`.

#### 3. Add resilience

Every LLM call must have:

- a timeout
- retry logic with exponential backoff
- bounded attempts
- logged failure metadata

Read `guides/resilience-guide.md`.

#### 4. Add safety checkpoints

If your agent sends messages, writes data, triggers automation, changes records, or performs any action that cannot be trivially undone, add a human approval checkpoint before that step.

If your capstone has no irreversible action, write that explicitly and explain why.

Read `guides/safety-checkpoints-guide.md`.

### Verification

You have succeeded in Part 1 when all of the following are true:

- Your main README or `docs/agent-architecture-lab7.md` states the chosen pattern and why it fits
- Your repo contains an explicit `AgentState` schema
- Your LLM wrapper code shows timeouts and retries
- Your safety checkpoint logic is implemented or explicitly documented as not needed
- Your episode log schema includes retry and error fields

---

## Part 2: LangGraph Mini-Build (45 min)

### The Goal

Build a small orchestration proof before you attempt a large one.

### What to Build

Use the starter in `examples/langgraph-starter/` and implement this flow:

1. **Research node**  
   Gather or synthesize facts for the task.

2. **Write node**  
   Convert the research into a user-facing output.

3. **Conditional route**  
   If approval is required, send the flow to `human_review`. Otherwise end the run.

The starter already includes:

- a typed state object
- a simple graph
- placeholder nodes
- a route function
- a runnable `main.py`

Your job in the lab is to:

- run the starter successfully
- understand how nodes read and update shared state
- copy the pattern into your capstone or map it directly to your existing architecture

### Verification

You have succeeded in Part 2 when:

- the graph runs locally
- state transitions are visible in the terminal output
- you can explain what each node reads and writes
- you can point to the equivalent nodes or stages in your capstone

---

## Part 3: Capstone Integration and Close-Out (15 min)

Before leaving the room, your team must do all of the following:

- [ ] Update the project README with an **Agent Architecture** section
- [ ] Commit the architecture doc, state schema, and resilience code
- [ ] Extend the episode log schema and commit the change
- [ ] Tag the repo

```bash
git add .
git commit -m "lab7: agent architecture, retries, checkpoint, langgraph mini-build"
git tag lab7-agent-architecture-checkpoint
git push origin main --tags
```

---

## File Map

```text
Lab-7/
├── README.md
├── QUICKSTART.md
├── GRADING-RUBRIC.md
├── INSTRUCTOR-GUIDE.md
│
├── templates/
│   ├── agent-architecture-template.md
│   ├── agentstate-template.md
│   ├── safety-checkpoint-template.md
│   ├── episode-log-extension.md
│   └── lab7-checklist.md
│
├── guides/
│   ├── agent-patterns-guide.md
│   ├── resilience-guide.md
│   ├── safety-checkpoints-guide.md
│   ├── langgraph-guide.md
│   └── openclaw-lessons-guide.md
│
└── examples/
    ├── langgraph-starter/
    ├── fastapi-scaffold/
    └── nextjs-scaffold/
```

---

## No New Homework From Lab 7

There is no separate homework submission from this lab. The purpose of Lab 7 is to harden your capstone before the midterm and before the Week 11 audit.

What you build here should still exist in your repo after the midterm. Do not treat this lab as a throwaway exercise.

---

## What This Sets Up

Lab 7 is the bridge between:

- Week 7, where you added streaming and conversation state
- Week 8, where you add orchestration, retries, and safety
- Week 11, where you must defend your safety and evaluation work with real evidence from your codebase and logs

If your team leaves Lab 7 with only a diagram and no code, you are behind.  
If your team leaves Lab 7 with code but no documented pattern, you are also behind.  
You need both.

---

*Lab 7 package for CS-AI-2025, Spring 2026.*

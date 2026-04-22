# Agent Patterns Guide

This guide helps you choose the correct architecture for Lab 7.

Do not start with the question, "How do I use many agents?"  
Start with the question, "What coordination problem does my capstone have?"

---

## Pattern 1: Orchestrator / Specialist

### Shape

One agent or controller receives the user request, decomposes it, delegates focused sub-tasks, and synthesizes the final answer.

### Use this when

- the task has separable subproblems
- the final answer needs synthesis across sources or viewpoints
- one specialist needs a different prompt, tool, or policy from another

### Example

A research assistant that:
- retrieves documents
- extracts facts
- drafts a summary

The orchestrator decides order and merges results.

### Strengths

- clear division of labour
- easier prompt specialization
- failure in one specialist does not require redesign of the whole system

### Weaknesses

- more moving parts
- more logging needed
- synthesis quality becomes its own problem

### Good capstone fit

- document analysis
- comparison workflows
- extract then explain workflows
- multi-source research tools

---

## Pattern 2: Supervisor / Worker

### Shape

A supervisor launches repeated worker tasks, monitors results, retries failures, and decides when enough work is complete.

### Use this when

- many tasks are similar
- work can happen in parallel
- resilience matters more than rich reasoning in each branch

### Example

A grading or evaluation system that:
- sends 20 prompts to a judge model
- retries failures
- aggregates the scores

### Strengths

- good for bulk work
- easy to monitor
- good fit for retries, quotas, and circuit breakers

### Weaknesses

- less natural for deep multi-step reasoning
- weak synthesis unless a separate summarizer exists

### Good capstone fit

- batch classification
- bulk evaluation
- scraping or retrieval jobs
- repeated tool calls over many items

---

## Pattern 3: Peer / Pipeline

### Shape

Agents operate in a fixed sequence. Each stage transforms the output and passes it forward.

### Use this when

- task order is strict
- output of one stage is the required input of the next
- the flow is stable and predictable

### Example

A workflow that:
1. transcribes audio
2. extracts entities
3. creates a structured report

### Strengths

- easy to understand
- easy to debug
- each stage has a narrow contract

### Weaknesses

- brittle if one stage produces bad output
- later stages inherit upstream errors
- less flexible when tasks must branch dynamically

### Good capstone fit

- ETL-like flows
- transcription then extraction
- transform then format workflows

---

## Single-Agent Is Still Valid

Choose a single-agent architecture when:

- the problem is small
- no clear subtask boundaries exist
- specialist prompts would not materially improve results
- orchestration would add more code than value

A justified single-agent system is stronger than a forced multi-agent system.

---

## Decision Questions

Answer these as a team.

1. Does your task have independent subtasks that could run separately?
2. Does any step require a different tool set, prompt, or safety policy?
3. Does your system need retries over many similar tasks?
4. Is the flow sequential by nature?
5. Does any action require human approval?
6. Would a second agent reduce failure, or only add complexity?

---

## Recommendation Rule

Use this rule in Lab 7:

- If your workflow is simple, stay single-agent and document why.
- If you need synthesis across focused subtasks, use orchestrator/specialist.
- If you need repeated monitored work, use supervisor/worker.
- If the order is strict and stable, use peer/pipeline.

---

## What to Write in Your README

Your architecture section should answer four things:

1. Which pattern did we choose?
2. Why does this fit our task better than the alternatives?
3. What shared state moves through the system?
4. Where are timeout, retry, and safety checkpoint logic enforced?

Use `templates/agent-architecture-template.md`.

---

*Guide for Lab 7.*

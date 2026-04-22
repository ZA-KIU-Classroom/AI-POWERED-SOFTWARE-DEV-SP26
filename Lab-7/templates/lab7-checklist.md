# Lab 7 Close-Out Checklist

**Team checklist. Complete before you leave the room.**

---

**Team name:**  
**Date:** Friday 24 April 2026

---

## Architecture

- [ ] We chose an agent pattern and documented why it fits our capstone
- [ ] We explicitly stated whether single-agent would or would not be enough
- [ ] We defined an `AgentState` object with named and typed fields
- [ ] We documented the architecture in the README or a `docs/` file

## Resilience

- [ ] Every LLM call now has a timeout
- [ ] Every external AI call now has bounded retries
- [ ] Retry count is visible in code and in the log schema
- [ ] We know which errors retry and which errors fail immediately

## Safety

- [ ] We identified the riskiest action in our capstone
- [ ] We added a human checkpoint, or documented clearly why none is needed
- [ ] We restricted tool access by role or stage
- [ ] We extended the episode log to include approval and error metadata

## Mini-Build

- [ ] We ran the LangGraph starter or equivalent orchestration proof
- [ ] We understand what each node reads and writes
- [ ] We can explain the route condition

## Repo Hygiene

- [ ] Code and docs are committed
- [ ] We tagged the repo `lab7-agent-architecture-checkpoint`
- [ ] We pushed the tag
- [ ] We know what still needs to be finished before Week 11

---

## Team Reflection

**The biggest architecture decision we made today was:**

```text
[answer]
```

**The biggest unresolved risk before Week 11 is:**

```text
[answer]
```

---

*Checklist for Lab 7.*

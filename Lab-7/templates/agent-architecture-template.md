# Agent Architecture Section Template

Copy this into your main README or into `docs/agent-architecture-lab7.md`.

---

## Agent Architecture

### 1. Chosen Pattern

**Pattern name:**  
`[orchestrator/specialist | supervisor/worker | peer/pipeline | justified single-agent]`

### 2. Why This Pattern Fits Our Capstone

Answer in 5 to 8 sentences:

- What coordination problem are we solving?
- Why is this pattern better than the alternatives?
- What complexity does it add?
- Why is that complexity worth it?

### 3. Main Stages or Nodes

| Stage / Node | Purpose | Reads from state | Writes to state | Tools allowed |
|---|---|---|---|---|
| `user_input` | | | | |
| `research` | | | | |
| `write` | | | | |
| `human_review` | | | | |
| `final_response` | | | | |

Delete rows you do not use.

### 4. Shared State

Link to the actual schema file:

`[path/to/agent_state.py or agent-state.ts]`

Then explain in 3 to 5 sentences:
- which fields are essential
- which fields are derived
- which fields are safety-critical

### 5. Timeout and Retry Policy

Document:

- timeout per model call
- max retry count
- which errors retry
- which errors fail immediately
- where this logic lives in code

### 6. Safety Checkpoint

Document:

- the riskiest action in the system
- whether human approval is required
- where in the flow the checkpoint happens
- what is logged when approval is granted or denied

### 7. Failure and Degradation Plan

State what happens if:

- retrieval fails
- the model times out
- one specialist fails
- approval is denied

### 8. What We Still Need Before Week 11

List 3 to 5 remaining gaps.

---

*Template for Lab 7.*

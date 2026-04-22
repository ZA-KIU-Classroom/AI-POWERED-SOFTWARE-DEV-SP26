# Lab 7 Grading Rubric

**Lab:** Lab 7, Agents, Orchestration, Resilience, and Safety  
**Course:** CS-AI-2025, Building AI-Powered Applications, Spring 2026  
**Graded as:** Capstone progress checkpoint feeding Week 11 Safety and Evaluation Audit and Week 15 Repository Review  
**Submission:** Team repo tagged `lab7-agent-architecture-checkpoint`

> Lab 7 does not carry a standalone point value. The work produced here becomes evidence for the Week 11 Safety and Evaluation Audit and for the final repository review.

---

## What the Instructor Checks After Lab 7

### Check 1: Agent Architecture Is Documented

| Criterion | Passes | Fails |
|---|---|---|
| Pattern choice exists | README or doc clearly states orchestrator/specialist, supervisor/worker, peer/pipeline, or justified single-agent | No pattern named |
| Pattern is justified | Team explains why this pattern fits the capstone task and rejects at least one weaker alternative | Pattern name appears but with no reasoning |
| State is explicit | `AgentState` or equivalent schema exists with named fields | State lives only in ad hoc dicts or comments |

---

### Check 2: Resilience Exists in Code

| Criterion | Passes | Fails |
|---|---|---|
| Timeout wrapper exists | Every LLM call goes through a timeout boundary | Raw provider calls with no timeout |
| Retry wrapper exists | External AI calls use bounded exponential backoff | No retry logic or infinite retry loop |
| Retry count is visible | Code and logs capture attempt count | Retries happen silently or are not logged |

---

### Check 3: Safety Checkpoint Exists

| Criterion | Passes | Fails |
|---|---|---|
| Irreversible actions identified | Team explicitly names the risky step, or explicitly documents there is none | No statement either way |
| Human approval logic exists | Approval gate or manual checkpoint is present before high-stakes action | Risky step runs automatically |
| Least-privilege reasoning exists | Team documents why each agent has the tools it has | Every agent gets every tool by default |

---

### Check 4: Episode Log Supports Audit Work

| Criterion | Passes | Fails |
|---|---|---|
| Errors are logged | Failure events exist as first-class log entries | Only success paths are logged |
| Timeout metadata exists | Logs include timeout values or timeout events | Timeout policy exists only in prose |
| Retry metadata exists | Logs include retry count and attempt outcomes | Retries occur but produce no trace |
| Approval metadata exists | Logs capture whether approval was required and granted | No evidence of checkpoint behaviour |

---

### Check 5: Mini-Build Was Completed

| Criterion | Passes | Fails |
|---|---|---|
| Two-node orchestration proof exists | LangGraph starter or raw equivalent runs locally | No orchestration proof exists |
| Shared state is visible | Team can explain what each node reads and writes | Nodes are treated as magic black boxes |
| Conditional route exists | Flow can branch to a human review step or equivalent checkpoint | All flows are linear with no decision point |

---

## Common Problems That Hurt the Week 11 Audit

1. **Pattern chosen for fashion, not fit**  
   Teams sometimes force multi-agent architecture into a simple problem. If one agent is enough, say so and defend it.

2. **Retries without limits**  
   An unbounded retry loop is a production bug, not resilience.

3. **Timeout value defined but never used**  
   Configuration alone does not count. The timeout must wrap the call.

4. **Safety gate exists only in the README**  
   If approval matters, the code must reflect that.

5. **Logs capture only happy-path runs**  
   Week 11 requires evidence of what happens under error conditions.

---

## Suggested Instructor Test

1. Ask the team to point to their architecture document.  
2. Ask them to show the timeout wrapper.  
3. Ask them to show the retry wrapper.  
4. Ask them to trigger or simulate a failure.  
5. Ask them where approval would happen before a risky action.  
6. Ask them where this is visible in the logs.

If they cannot answer those six questions in under five minutes, the architecture is not mature enough yet.

---

*Grading rubric for Lab 7, CS-AI-2025.*

# Lab 6 Grading Rubric

**Lab:** Lab 6 — Streaming, Memory, and MCP
**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026
**Graded as:** Capstone progress checkpoint — feeds into Safety and Evaluation Audit (Week 11) and Repository Review (Week 15)
**Submission:** `lab6-mcp-checkpoint` tag pushed to team repo + individual `mcp-reflection.md` committed to personal repo

> Lab 6 does not have a standalone point value. It is a capstone progress checkpoint. The deliverables produced here feed directly into the **Safety and Evaluation Audit (5 pts, Week 11)** and **Repository Review (10 pts, Week 15)**. Skipping or rushing Lab 6 creates compounding technical debt that is very difficult to recover from.

---

## What the Instructor Checks After Lab 6

### Check 1: Streaming Endpoint

**Verified by:** Clone repo, add `.env`, start app, send a request, observe the response

| Criterion | Passes | Fails |
|---|---|---|
| Endpoint exists and returns `text/event-stream` content type | Route responds without 404 or 500 | Route missing or crashes on streaming request |
| Tokens arrive before the full response is complete | First token visible within 2 seconds of request | Full response appears at once (blocking behaviour) |
| `[DONE]` sentinel emitted at stream end | Client receives the done signal | Stream hangs open or client never knows it finished |
| Episode log captures `stream_start_ms` and `stream_end_ms` | Both fields present in log | Fields absent or hardcoded to zero |

---

### Check 2: Session Memory

**Verified by:** Sending a multi-turn conversation and inspecting responses

| Criterion | Passes | Fails |
|---|---|---|
| Session persists across turns | Agent refers to information from earlier in the conversation | Agent treats every message as a new, context-free conversation |
| History is passed on every call | Messages array contains more than just the latest user message | Only the latest message is sent to the model each time |
| Trim strategy implemented | Codebase shows a sliding window, summarisation, or explicit trim | History grows unboundedly with no trim logic present |

**Test to run:**

```
Turn 1: "My name is [your name] and I am building a [describe your capstone]."
Turn 2: "What is my name?"
Turn 3: "What am I building?"
Turn 5: "Summarise everything you know about me."
```

All four questions must produce correct answers using information from earlier turns.

---

### Check 3: MCP Server (Team)

**Verified by:** Running the MCP server via stdio and connecting with MCP Inspector or Cursor

| Criterion | Passes | Fails |
|---|---|---|
| `mcp-server/` folder exists in team repo | Folder present with at least one source file | Folder missing or empty |
| Server starts without errors | `node src/server.js` or `python server.py` runs cleanly | ImportError, ModuleNotFoundError, or crash on startup |
| Tool is discoverable | MCP Inspector shows at least one tool with a name and description | No tools listed, or tools appear with empty descriptions |
| Tool executes and returns a result | Calling the tool via MCP Inspector returns a non-empty content array | Tool call returns an error or empty string |
| `lab6-mcp-checkpoint` tag exists | `git tag | grep lab6-mcp-checkpoint` returns the tag | Tag missing or points to a commit before MCP code was added |

---

### Check 4: MCP Reflection (Individual)

**Verified by:** Checking each team member's personal repo

| Criterion | Full marks | Partial | No marks |
|---|---|---|---|
| File exists | `mcp-reflection.md` present in personal repo root | File present but empty or less than 100 words | File absent |
| Question 1 — Tool selection rationale | Explains specifically which function was chosen and why, referencing the tool decision framework from the lecture | Vague explanation without reference to specific criteria | Not answered |
| Question 2 — Security considerations | Identifies at least two concrete security risks and states mitigations | One risk identified, or risks named without mitigations | Not answered or generic |
| Question 3 — Protocol comparison | Draws a specific contrast between raw function calling (Week 6) and the MCP protocol wrapper | Generic observation with no specific technical comparison | Not answered |
| Word count | 200–300 words | Under 200 or over 300 | Under 50 |

---

## Common Issues That Create Problems in Week 11

These are not graded today but they create debt you will pay at the Safety and Evaluation Audit:

1. **Episode log not capturing streaming calls.** The audit requires cost data for streaming specifically. If you only log blocking calls, you will have a gap in your audit data that is difficult to explain.

2. **MCP server has no input validation.** Any argument your tool receives from the model must be validated before it is used. A model can pass unexpected argument types. Your server should handle this gracefully.

3. **MCP server exposes a destructive function.** If you wrapped a write, delete, or send function as your MCP tool, it needs an explicit confirmation step. Read-only tools are safer choices for a first MCP implementation.

4. **Session state lives only in process memory.** This is acceptable for Lab 6. But note it in your session design document — if your server restarts, all sessions are lost. Week 12 production content will address persistence.

5. **MCP reflection is too short or generic.** The reflection feeds Week 11. The grader will compare it against your actual code. A reflection that says "I learned a lot about MCP" without technical specifics will receive zero marks.

---

*Grading rubric for CS-AI-2025 Lab 6, Spring 2026.*

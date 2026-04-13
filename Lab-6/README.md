# Lab 6: Streaming, Memory, and MCP

**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026
**Lab Date:** Friday 17 April 2026
**Group A:** 09:00 – 11:00 | **Group B:** 11:00 – 13:00
**Location:** Computer Lab / Bring Your Own Laptop

---

## What This Lab Is

Lab 5 gave your capstone a working AI endpoint. Lab 6 makes it feel alive.

By the end of this session, your team must have:

1. A **streaming endpoint** delivering tokens to the UI in real time — not a blocking response
2. A **session memory** that preserves conversation history across turns
3. At least one capstone backend function **wrapped as an MCP server tool** and committed to your team repo
4. An **individual MCP reflection** committed to each person's personal repo

This lab has two distinct components: a team sprint (Parts 1 and 2) and an individual written component (Part 3). Both are required.

---

## Before You Arrive

All of the following must be done before lab starts. Do not use lab time for these.

- [ ] Lab 5 endpoint committed and tagged — run it locally and confirm it returns a real AI response
- [ ] OpenRouter key still working — test it with a curl call before Friday morning
- [ ] Your MCP tool candidate decided — which one capstone function will you wrap today?
- [ ] Node 18+ confirmed (for TypeScript MCP server) or Python 3.10+ confirmed (for Python MCP server)
- [ ] Team repo cloned and environment running on every laptop that will be used today

If your OpenRouter key has stopped working, email `zeshan.ahmad@kiu.edu.ge` before Friday morning.

---

## Lab Structure

| Time | Activity | Duration |
|------|----------|----------|
| :00  | Arrival, setup checks, blockers queue | 5 min |
| :05  | Lab intro and objectives | 5 min |
| :10  | **Part 1:** Streaming sprint — add stream=True, wire up SSE endpoint | 45 min |
| :55  | **Part 2:** Session memory — implement conversation state across turns | 30 min |
| :85  | **Part 3:** MCP mini-build — wrap one function, commit, write reflection | 30 min |
| :115 | Commit, tag, push, and close out | 5 min |
| :120 | End of lab | |

*Times are from session start — Group A 09:00, Group B 11:00.*

---

## Part 1: Streaming Sprint (45 min)

### The Goal

By the 45-minute mark, your primary AI endpoint must deliver responses as a token stream. The first token must appear in the browser within 500ms of sending the request.

### What to Build

**Backend — add a streaming route:**

```bash
# FastAPI: see examples/fastapi-scaffold/routers/stream_router.py
# Next.js: see examples/nextjs-scaffold/app/api/chat/stream/route.ts
```

Your streaming endpoint must:

- Accept a JSON body with at least `message` (string) and `session_id` (string)
- Return `Content-Type: text/event-stream`
- Emit tokens as `data: {"token": "..."}` events
- Emit `data: [DONE]` when the stream is finished
- Log `stream_start_ms`, `stream_end_ms`, and token count to your episode log

**Frontend — consume the stream:**

```javascript
// See examples/ for a complete working implementation
// The key pattern:
const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  // decode and append each token to your UI state
}
```

### Verification

You have succeeded when:

1. A user types a message and sees the first word appear in under 500ms
2. The rest of the response streams in word by word
3. The terminal shows a cost log entry for the streaming call

---

## Part 2: Session Memory (30 min)

### The Goal

Your agent must remember the conversation. If a user says "my name is Nino" in turn 1, the agent must be able to refer to Nino in turn 5 — without the user repeating themselves.

### What to Build

Implement in-memory session storage with a sliding window trim:

```python
# See examples/fastapi-scaffold/services/session_service.py for the full implementation
sessions: dict[str, list] = {}   # session_id -> message history

def load_session(session_id: str) -> list:
    return sessions.get(session_id, [])

def save_session(session_id: str, messages: list):
    # Keep system prompt + last 20 turns (40 messages)
    trimmed = messages[:1] + messages[-40:] if len(messages) > 41 else messages
    sessions[session_id] = trimmed
```

Every request to your streaming endpoint must:

1. Load the session history for this `session_id`
2. Append the new user message
3. Pass the full trimmed history to the model (not just the latest message)
4. Append the assistant response to the history
5. Save the updated session

### Verification

Send 5 messages in the same session referencing earlier messages. The agent should demonstrate it remembers what was said in turn 1 when responding in turn 5.

---

## Part 3: MCP Mini-Build (30 min)

This is the most important part of today for your capstone's long-term architecture.

### Team Component (in-lab)

Pick one function from your Lab 5 capstone endpoint. Wrap it as a minimal MCP server tool.

**Criteria for choosing your function:**

- The AI should decide *when* to call it based on user intent (not always)
- It returns real data — not a hardcoded string
- It is a function your team already wrote and understands

**Build steps:**

```bash
# TypeScript (recommended if your team is on Next.js)
# See examples/mcp-server-typescript/

# Python (recommended if your team is on FastAPI)
# See examples/mcp-server-python/
```

Your MCP server must:

- Expose at least one tool with a clear name and description
- Accept typed arguments
- Return a result the model can read
- Run locally via stdio transport and be discoverable by Cursor or Claude Desktop

**Commit to your team repo:**

```bash
# Place the MCP server code in your team repo under:
mcp-server/

# Then:
git add .
git commit -m "lab6: streaming endpoint + session memory + mcp server scaffold"
git tag lab6-mcp-checkpoint
git push origin main --tags
```

### Individual Component (each person, personal repo)

Every team member must write an individual reflection and commit it to their **personal repo** (not the team repo) before the end of lab.

**File:** `mcp-reflection.md` in your personal repo root

**Required content (200–300 words):**

1. Which capstone function did you wrap as an MCP tool, and why did you choose that function over the others?
2. What security considerations did you apply? What would you expose differently if this MCP server were public on the internet?
3. What surprised you about the MCP protocol structure compared to the raw function calling you built in Week 6?

This reflection feeds directly into the Safety and Evaluation Audit in Week 11. The quality of your answer matters — this is not a checkbox.

---

## File Map

```
Lab-6/
├── README.md                              ← You are here
├── QUICKSTART.md                          ← Environment check for streaming and MCP
├── GRADING-RUBRIC.md                      ← How this lab feeds your capstone grade
├── INSTRUCTOR-GUIDE.md                    ← For the instructor and TAs
│
├── templates/
│   ├── session-design.md                  ← Team: document your session memory decisions
│   ├── mcp-reflection.md                  ← Individual: MCP reflection template
│   ├── episode-log-template.md            ← Extend your cost log to capture streaming events
│   └── lab6-checklist.md                  ← Individual close-out checklist
│
├── guides/
│   ├── streaming-guide.md                 ← SSE, token delivery, cancellation, backpressure
│   ├── session-memory-guide.md            ← Short-term memory patterns and trim strategies
│   ├── mcp-setup-guide.md                 ← Installing SDK, writing a tool, testing with Cursor
│   └── episode-log-guide.md               ← Extending cost logging for streaming and tool calls
│
└── examples/
    ├── fastapi-scaffold/                  ← Streaming + session extensions for FastAPI
    │   ├── routers/stream_router.py
    │   ├── services/session_service.py
    │   ├── services/episode_logger.py
    │   └── .env.example
    ├── nextjs-scaffold/                   ← Streaming + session extensions for Next.js
    │   ├── app/api/chat/stream/route.ts
    │   ├── lib/session-store.ts
    │   └── lib/episode-logger.ts
    ├── mcp-server-python/                 ← Minimal Python MCP server scaffold
    │   ├── server.py
    │   ├── pyproject.toml
    │   └── README.md
    └── mcp-server-typescript/             ← Minimal TypeScript MCP server scaffold
        ├── src/server.ts
        ├── package.json
        ├── tsconfig.json
        └── README.md
```

---

## What a Successful Lab 6 Looks Like

At the end of lab, an instructor should be able to:

1. Clone your team repo, add a `.env` file, start the app with one command
2. Send a message to your streaming endpoint and watch tokens appear in real time
3. Send a follow-up message referencing the first — the agent should remember
4. Run `npx @modelcontextprotocol/inspector` or open Cursor's MCP config and see your tool listed
5. Invoke your MCP tool and see a real result returned

And separately, each team member's personal repo should have a committed `mcp-reflection.md`.

---

## Resources

**In This Lab Folder:**
- `QUICKSTART.md` — fast environment check for streaming and MCP
- `guides/streaming-guide.md` — complete SSE implementation reference
- `guides/mcp-setup-guide.md` — MCP SDK installation and tool registration

**External:**
- [MCP SDK (TypeScript)](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP SDK (Python)](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Inspector (testing tool)](https://github.com/modelcontextprotocol/inspector)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Course GitHub](https://github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26)

**Questions:**
- During lab: raise your hand or use the help queue on the board
- After lab: post in the course forum
- Email: `zeshan.ahmad@kiu.edu.ge` — response within 48 hours on weekdays

---

*Lab 6 materials for CS-AI-2025 Spring 2026.*
*Maintained at [github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26](https://github.com/ZA-KIU-Classroom/AI-POWERED-SOFTWARE-DEV-SP26)*

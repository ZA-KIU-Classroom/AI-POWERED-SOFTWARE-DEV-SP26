# Session Memory Guide

**CS-AI-2025 Lab 6, Spring 2026**

---

## What Session Memory Is

Session memory is the conversation history you pass to the model on every turn. Without it, every message is a fresh conversation. With it, the model can refer to anything the user has said earlier in the session.

The model has no built-in memory. Everything it "knows" about the current conversation must be in the `messages` array you send. Your job is to maintain that array correctly.

---

## The Core Pattern

```python
# On every turn:
# 1. Load history
# 2. Append new user message
# 3. Call model with full history
# 4. Append assistant response
# 5. Save updated history

messages = load_session(session_id)

if not messages:
    messages = [{"role": "system", "content": system_prompt}]

messages.append({"role": "user", "content": user_input})

response = call_model(messages)       # full history, not just the latest message

messages.append({"role": "assistant", "content": response})

save_session(session_id, messages)
```

The single most common mistake is passing only `[{"role": "user", "content": user_input}]` instead of the full history. This produces an agent that has amnesia on every turn.

---

## In-Memory Implementation (Lab 6 Default)

For Lab 6, in-memory storage is sufficient. The session disappears when the server restarts — this is a known limitation, documented below.

**Python (FastAPI):**

```python
# services/session_service.py
from typing import List, Dict, Any

# In-process store: session_id -> message list
_sessions: dict[str, list] = {}

# Keep at most 20 turns (40 messages) plus the system prompt
_MAX_MESSAGES = 41


def load_session(session_id: str) -> list:
    """Return the message history for a session, or an empty list."""
    return list(_sessions.get(session_id, []))


def save_session(session_id: str, messages: list) -> None:
    """Save the message history, applying the sliding window trim."""
    _sessions[session_id] = _trim(messages)


def delete_session(session_id: str) -> None:
    """Delete all history for a session (user-initiated reset)."""
    _sessions.pop(session_id, None)


def _trim(messages: list) -> list:
    """
    Keep the system prompt (index 0) and the last N messages.
    This prevents the context window from growing unboundedly.
    """
    if len(messages) <= _MAX_MESSAGES:
        return messages

    system_messages = [m for m in messages if m["role"] == "system"]
    non_system      = [m for m in messages if m["role"] != "system"]

    # Keep the most recent non-system messages
    trimmed_non_system = non_system[-((_MAX_MESSAGES - len(system_messages))):]

    return system_messages + trimmed_non_system
```

**TypeScript (Next.js):**

```typescript
// lib/session-store.ts

type Message = { role: "system" | "user" | "assistant"; content: string };

const _sessions = new Map<string, Message[]>();
const MAX_MESSAGES = 41;

export function loadSession(sessionId: string): Message[] {
  return [...(_sessions.get(sessionId) ?? [])];
}

export function saveSession(sessionId: string, messages: Message[]): void {
  _sessions.set(sessionId, trim(messages));
}

export function deleteSession(sessionId: string): void {
  _sessions.delete(sessionId);
}

function trim(messages: Message[]): Message[] {
  if (messages.length <= MAX_MESSAGES) return messages;

  const system    = messages.filter(m => m.role === "system");
  const nonSystem = messages.filter(m => m.role !== "system");
  const keep      = nonSystem.slice(-(MAX_MESSAGES - system.length));

  return [...system, ...keep];
}
```

---

## Generating and Managing Session IDs

The client is responsible for creating and sending the `session_id`. A simple UUID works well.

**Frontend (browser):**

```typescript
// Generate once per conversation, store in localStorage or component state
function getOrCreateSessionId(): string {
  let id = sessionStorage.getItem("session_id");
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem("session_id", id);
  }
  return id;
}
```

**Why sessionStorage, not localStorage:**
`sessionStorage` clears when the tab closes. This means each new browser tab starts a fresh conversation automatically. `localStorage` would persist across tabs and browser restarts — use that only if you want cross-session persistence (which requires a proper database, not in-memory storage).

---

## Verifying Session Memory Works

Run this exact conversation in your app and verify each answer:

```
Turn 1: "My favourite programming language is Python and I am building a restaurant booking system."
Turn 2: "What is my favourite language?"    → Agent should answer: Python
Turn 3: "What am I building?"               → Agent should answer: restaurant booking system
Turn 4: "Tell me about the history of that language."  → Agent should discuss Python
Turn 5: "What are some good libraries for my project?" → Agent should suggest Python libraries for booking systems
```

If the agent fails any of these, the history is not being passed correctly. Add a debug log before the model call:

```python
print(f"[SESSION] Sending {len(messages)} messages to model")
for m in messages:
    print(f"  [{m['role']}] {m['content'][:60]}...")
```

---

## Trim Strategy Comparison

Three strategies, each with a different tradeoff:

| Strategy | How it works | Best for | Tradeoff |
|---|---|---|---|
| **Sliding window** | Keep system prompt + last N messages | Most capstone apps | Simple. Loses early context after many turns. |
| **Summarise-and-compress** | When window hits 80% capacity, call model to summarise old turns, replace with summary | Long-running sessions where early context matters | Costs one extra model call per compression event. |
| **Pinned messages** | Mark certain messages as never-trimmable | When specific facts must always survive | Requires your code to track which messages are pinned. |

For Lab 6, implement the **sliding window**. The other two strategies are relevant for your Week 11 audit discussion.

---

## Known Limitations of In-Memory Storage

Document these in your `templates/session-design.md`:

1. **Server restart loses all sessions.** Every session is gone if the server crashes or redeploys. Users lose their conversation history. This is acceptable for a prototype.

2. **Multiple server instances cannot share sessions.** If your app runs on two Railway dynos, a user who connects to dyno A cannot access sessions created on dyno B. This breaks at production scale. Week 12 covers Redis as the fix.

3. **Memory grows with number of users.** In development with a few testers, this is fine. At 1,000 concurrent users with 40-message sessions, you are storing significant data in RAM. Plan accordingly.

4. **No user-controlled deletion.** In production, users must be able to request deletion of their session data. Your `delete_session()` function is the mechanism — expose it via an API endpoint.

---

## Privacy Requirements

From the Week 7 lecture and the syllabus:

- Session memory must implement user-controlled deletion before Week 11
- No cross-session data access — user A must never see user B's history
- Voice audio must never be stored in session history — store the transcription only
- Document your data retention policy in your capstone README

---

*Session memory guide for CS-AI-2025 Lab 6, Spring 2026.*

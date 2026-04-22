# AgentState Template

Use this template to define the shared state object for your capstone.

Do not add fields because they sound useful.  
Add fields only if a node reads or writes them.

---

## Recommended Minimum Fields

| Field | Type | Required | Why it exists |
|---|---|---|---|
| `session_id` | `str` or `string` | Yes | Ties the run to a conversation |
| `user_request` | `str` or `string` | Yes | Original task from the user |
| `messages` | `list[dict]` or `Message[]` | Yes | Conversation history |
| `current_step` | `str` or `string` | Yes | Shows where the flow is |
| `approval_required` | `bool` | Yes | Safety routing |
| `approved` | `bool | None` | Yes | Human review outcome |
| `retry_count` | `int` | Yes | Resilience evidence |
| `timeout_ms` | `int` | Yes | Enforced timeout policy |
| `last_error` | `str | None` | Yes | Failure visibility |
| `final_response` | `str | None` | Yes | User-facing output |

Add domain fields below this line.

---

## Python Example

```python
from typing import TypedDict

class AgentState(TypedDict, total=False):
    session_id: str
    user_request: str
    messages: list[dict]
    current_step: str
    approval_required: bool
    approved: bool | None
    retry_count: int
    timeout_ms: int
    last_error: str | None
    final_response: str | None
    research_notes: str | None
```

## TypeScript Example

```ts
export interface AgentState {
  sessionId: string;
  userRequest: string;
  messages: Array<{ role: string; content: string }>;
  currentStep: string;
  approvalRequired: boolean;
  approved: boolean | null;
  retryCount: number;
  timeoutMs: number;
  lastError: string | null;
  finalResponse: string | null;
  researchNotes?: string | null;
}
```

---

## Team Notes

**Fields we added for our capstone:**

- `[field name]`
- `[field name]`
- `[field name]`

**Fields we deliberately did not add:**

- `[field name] because ...`

---

*Template for Lab 7.*

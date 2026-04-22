# Lab 7 Quickstart

**Verify your baseline for orchestration in 10 to 15 minutes.**

This is a pre-flight check. It assumes Lab 6 is already working.

---

## Step 1: Confirm Your Lab 6 Streaming Endpoint Still Works

**FastAPI**

```bash
cd your-team-repo/backend
uv run uvicorn main:app --reload --port 8000

curl -N -X POST http://localhost:8000/api/ai/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Reply with the words: lab6 stream alive","session_id":"lab7-check"}'
```

**Next.js**

```bash
cd your-team-repo
npm run dev

curl -N -X POST http://localhost:3000/api/ai/stream \
  -H "Content-Type: application/json" \
  -d '{"message":"Reply with the words: lab6 stream alive","session_id":"lab7-check"}'
```

You should see tokens arrive progressively. If the whole response appears at once, do not start Lab 7 work yet.

---

## Step 2: Confirm Session Memory Still Works

In the same session, send:

1. `My project is a travel planning assistant.`
2. `What project am I building?`

If the second answer does not correctly refer to the first, your baseline is broken.

---

## Step 3: Decide Your Agent Pattern Before Lab Starts

Write one sentence in your team notes before Friday:

- Which pattern are you choosing?
- Why is that better than the other two patterns for your project?

If you arrive undecided, you will lose time.

---

## Step 4: Extend the Episode Log Schema

Before lab, confirm that your log can hold these fields:

| Field | Type | Why it matters |
|---|---|---|
| `event_type` | string | Distinguishes model call, retry, timeout, approval, error |
| `success` | boolean | Separates good runs from failed runs |
| `retry_count` | integer | Required for resilience analysis |
| `timeout_ms` | integer | Proves timeout policy is real |
| `latency_ms` | integer | Needed for observability |
| `error_type` | string or null | Helps build error taxonomy later |
| `approval_required` | boolean | Supports safety audit evidence |
| `approved` | boolean or null | Shows human checkpoint outcome |

Use `templates/episode-log-extension.md`.

---

## Step 5: Install LangGraph on One Machine Per Team

The mini-build is Python-first. Even if your capstone is in Next.js, one machine in the team should be able to run the LangGraph starter.

```bash
cd examples/langgraph-starter
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

If your shell is PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If `python main.py` runs and prints state transitions, you are ready.

---

## Step 6: Know Where the New Files Will Live in Your Repo

Before lab, decide the target locations in your capstone repo:

```text
docs/agent-architecture-lab7.md
backend/services/retry_utils.py
backend/schemas/agent_state.py
backend/services/approval.py
logs/episode-log-lab7.md
```

Or the equivalent structure for Next.js:

```text
docs/agent-architecture-lab7.md
lib/retry.ts
lib/agent-state.ts
lib/guardrails.ts
logs/episode-log-lab7.md
```

Do not waste lab time arguing about folder names.

---

## You Are Ready

If all six steps passed, your team is ready to use Lab 7 for real architecture work instead of emergency repair.

If any step failed, fix it before the lab starts.

---

*Quickstart for Lab 7, CS-AI-2025.*

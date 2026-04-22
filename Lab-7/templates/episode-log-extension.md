# Episode Log Extension Template

Lab 7 extends the logging work from earlier labs.

Your team does not need a perfect production logger today.  
Your team does need an episode log schema that supports Week 11.

---

## Minimum Fields for Lab 7

| Field | Type | Example | Why it matters |
|---|---|---|---|
| `event_type` | string | `model_call`, `retry`, `timeout`, `approval_requested`, `approval_denied`, `error` | Separates kinds of events |
| `session_id` | string | `9db0...` | Traceability |
| `model` | string | `google/gemini-2.5-flash` | Provider analysis |
| `success` | boolean | `true` | Happy path vs failure |
| `retry_count` | integer | `2` | Resilience evidence |
| `timeout_ms` | integer | `8000` | Timeout policy evidence |
| `latency_ms` | integer | `1350` | Performance analysis |
| `error_type` | string or null | `timeout_error` | Error taxonomy |
| `approval_required` | boolean | `true` | Safety evidence |
| `approved` | boolean or null | `false` | Checkpoint outcome |
| `cost_usd` | number | `0.0021` | Cost tracking continuity |

---

## Markdown Log Example

```md
| ts | event_type | session_id | model | success | retry_count | timeout_ms | latency_ms | error_type | approval_required | approved | cost_usd | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-04-24T09:32:10Z | model_call | abc-123 | google/gemini-2.5-flash | true | 0 | 8000 | 1120 |  | false |  | 0.0019 | research node |
| 2026-04-24T09:32:15Z | retry | abc-123 | google/gemini-2.5-flash | false | 1 | 8000 | 8003 | timeout_error | false |  | 0.0000 | write node timed out |
| 2026-04-24T09:32:18Z | approval_requested | abc-123 |  | true | 0 | 0 | 0 |  | true |  | 0.0000 | ready to send email |
| 2026-04-24T09:32:25Z | approval_denied | abc-123 |  | true | 0 | 0 | 0 |  | true | false | 0.0000 | user cancelled |
```

---

## Team Action

Before leaving lab, confirm:

- [ ] we can log failure events
- [ ] we can log retry events
- [ ] we can log checkpoint events
- [ ] the schema lives in code or docs, not only in memory

---

*Template for Lab 7.*

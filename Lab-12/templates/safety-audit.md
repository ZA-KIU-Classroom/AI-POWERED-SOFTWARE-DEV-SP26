# Safety and Evaluation Audit

Append this lab's results to your existing `docs/safety-audit.md` from Week 11. Do not overwrite the earlier audit; add a "Lab 12 red-team pass" section so reviewers see the progression.

## Threat model summary

List the threats that apply to your capstone. Mark each as in scope or out of scope with one line of justification.

| Threat | In scope? | Why |
|---|---|---|
| Prompt injection (direct) | | |
| Prompt injection (indirect, via documents or tools) | | |
| Data exfiltration (secrets, other users' data) | | |
| Jailbreak (policy bypass) | | |
| Memory or RAG poisoning | | |

## Attacks run in Lab 12

For each attack you ran, record the exact input, what happened, and the control that handled it (or the fix you will make). See `examples/attacks.md` for the strings to try.

### Attack 1 · Direct prompt injection

- **Input used:**
  > 
- **What happened:**
  > 
- **Control that stopped it (or fix needed):**
  > 
- **Status:** held / partially held / got through

### Attack 2 · Indirect injection via a document

- **Input used:**
  > 
- **What happened:**
  > 
- **Control that stopped it (or fix needed):**
  > 
- **Status:** held / partially held / got through

### Attack 3 · Jailbreak attempt

- **Input used:**
  > 
- **What happened:**
  > 
- **Control that stopped it (or fix needed):**
  > 
- **Status:** held / partially held / got through

### Attack 4 · Data exfiltration or memory poisoning

- **Input used:**
  > 
- **What happened:**
  > 
- **Control that stopped it (or fix needed):**
  > 
- **Status:** held / partially held / got through

## Controls in place

Tick what is actually wired in, not what you intend to add.

- [ ] Input sanitization: user and document text is treated as data, wrapped in clear delimiters
- [ ] Output filtering: responses scanned for secrets and system-prompt leakage before display
- [ ] Least privilege on tools: each tool can only do the minimum it needs
- [ ] Sandboxing and limits: tool calls run with timeouts and rate limits
- [ ] Logging: every request leaves a trace, with `model_used` recorded

## Open issues for Demo Day

> 

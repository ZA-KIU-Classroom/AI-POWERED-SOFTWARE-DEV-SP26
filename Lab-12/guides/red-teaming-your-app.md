# Guide · Red Teaming Your Own App

Red teaming is deliberately attacking your own system to find weaknesses before someone else does. On Demo Day someone may paste a prompt injection or upload a poisoned document. Find those holes today, on your own terms.

## The attacker mindset

Your app trusts three things it should not: the user's text, the contents of any document or tool result, and its own memory. An attacker turns each of those into a weapon. Your job is to assume every input is hostile and prove your controls hold.

## The four attacks to run

Run each one against your deployed app and record the result in `docs/safety-audit.md` using `templates/safety-audit.md`. Concrete strings to paste are in `examples/attacks.md`.

### 1. Direct prompt injection

The user types an instruction that tries to override your system prompt, for example asking the model to ignore its rules and reveal its system prompt or a secret. Test whether your app leaks anything or changes behaviour.

### 2. Indirect prompt injection

A malicious instruction is hidden inside a document, a web page, or a tool result your agent reads. This is the ClawHavoc-class risk: the agent trusts a tool result and acts on a command buried in it. If your capstone ingests documents or calls tools, this is your highest-priority test.

### 3. Jailbreak

Role-play or obfuscation tries to get the model to do what your policy forbids ("you are a character with no rules, now..."). Test whether your guardrails survive a persona switch.

### 4. Data exfiltration or memory poisoning

The attacker tries to read another user's data or your secrets, or writes bad data into memory or RAG so future answers are corrupted. Test isolation between users and whether anything written to memory is validated.

## The four defenses

For every attack, there is a matching control. You do not need exotic defenses, you need the standard ones actually wired in.

| Defense | What it does |
|---|---|
| Input sanitization | Treat all user and document text as data, never as instructions. Wrap it in clear delimiters and tell the model that everything inside is untrusted content. |
| Output filtering | Scan responses for secrets, system-prompt leakage, and policy violations before they reach the user. |
| Least privilege on tools | A tool that can only act on the logged-in user's data cannot exfiltrate someone else's. Give each tool the minimum power it needs. |
| Sandboxing and limits | Run tool calls in a constrained environment with timeouts and rate limits. No single call gets unbounded power or time. |

## Reference

The OWASP Top 10 for LLM Applications is the industry checklist. Prompt injection is LLM01, the number one risk, for a reason. You do not need to memorise it, but naming it on your safety slide signals you did the homework.

## What to document

For each attack: the exact input you used, what happened, and the control that stopped it (or the fix you will make this week). An attack that gets through is a finding, not a failure, as long as you document it and fix it before Demo Day. A filled-in example is in `examples/sample-safety-audit.md`.

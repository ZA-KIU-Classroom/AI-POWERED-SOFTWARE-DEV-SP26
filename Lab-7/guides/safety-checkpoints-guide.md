# Safety Checkpoints Guide

Lab 7 safety is about system behaviour, not only model content.

The question is simple:

**What must the model never do automatically?**

---

## 1. The Irreversibility Spectrum

Not all actions carry the same risk.

| Action | Risk level | Typical checkpoint need |
|---|---|---|
| Read public data | Low | None |
| Query internal data | Low to medium | Auth and logging |
| Draft a message | Medium | User review if sensitive |
| Send a message | High | Human approval |
| Write to a database | High | Guardrail, auth, sometimes approval |
| Trigger automation | High | Human approval |
| Delete data | Critical | Human approval plus audit trail |

If your capstone reaches the right side of this table, you need a checkpoint.

---

## 2. Human-in-the-Loop Pattern

Use a human checkpoint when:

- the action is irreversible
- the action affects another person
- the action changes records
- the action spends money
- the action creates legal, academic, or health risk

### Minimal pattern

1. agent plans an action
2. system marks `approval_required = True`
3. action is shown to the user or operator
4. system stores `approved = True` or `False`
5. action runs only if approval is granted

---

## 3. Least Privilege

Do not give every agent every tool.

Examples:
- retrieval agent gets search only
- writing agent gets formatting only
- database write tool is available only to the final approved stage
- evaluation agent does not get delete or send privileges

This matters even in classroom prototypes.

---

## 4. Sandboxing

If a node executes code, accesses files, or uses browser automation, the environment must be constrained.

Lab 7 does not require a full sandbox implementation.  
Lab 7 does require the team to state:

- whether any node runs code or browser tasks
- what the trust boundary is
- what the future production control would be

---

## 5. What to Log for Safety

Your log should record:

- checkpoint requested
- who approved or denied
- when approval happened
- action name
- outcome
- failure if approval missing

If the checkpoint exists only in the UI and not in logs, it will be hard to defend in Week 11.

---

## 6. OpenClaw Lesson

A system can have impressive capability and still fail on trust boundaries.

What to copy:
- modular skill/tool layer
- separation of channels
- composable architecture

What not to copy:
- trust-by-default assumptions
- exposed keys
- unauthenticated local or admin interfaces
- unsafe execution surfaces

Read `guides/openclaw-lessons-guide.md`.

---

## 7. What to Write in Lab 7

Your team must state:

1. What is the riskiest action in our capstone?
2. Does it require approval?
3. Where in the flow does the checkpoint happen?
4. What gets logged?
5. If we do not need approval, why not?

Use `templates/safety-checkpoint-template.md`.

---

*Guide for Lab 7 safety checkpoints.*

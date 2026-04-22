# OpenClaw Lessons Guide

The lecture case study is useful because it separates **capability** from **trustworthiness**.

OpenClaw showed how fast a local-first agent product can spread.  
It also showed how quickly poor defaults become security problems.

This guide is not about reproducing the case study details.  
It is about extracting design lessons for your capstone.

---

## 1. What OpenClaw Got Right

### Local-first posture

Keeping data on the user's machine or inside the user's own environment can reduce privacy risk and simplify certain trust questions.

### Composable skills

The system treated tools or skills as modular components instead of baking everything into one monolith.

### Multi-provider flexibility

A system that can switch models or providers is more resilient than one locked to a single vendor.

### Fast builder iteration

The architecture showed that a small team can move quickly when the layers are separated clearly.

---

## 2. What OpenClaw Got Wrong

### Trust-by-default assumptions

Local or internal surfaces were treated as safe without enough verification.

### Poor boundary hardening

Sensitive paths and operational interfaces were too exposed.

### Dangerous defaults

Capabilities existed before the surrounding controls were mature.

### Weak auditability

When a system has strong powers, you need stronger logging and review.

---

## 3. What This Means for Your Capstone

Ask these questions:

1. Which of our interfaces do we currently trust too easily?
2. Which tool is most dangerous if called at the wrong time?
3. Which agent should definitely **not** have access to which tool?
4. Where would an approval checkpoint matter?
5. If our agent failed or was tricked, what evidence would remain in the logs?

---

## 4. Copy This

- modular architecture
- explicit skills or tools
- provider abstraction
- clean separation of stages
- local or user-controlled data where appropriate

## 5. Do Not Copy This

- exposed keys
- unauthenticated control paths
- execution without explicit policy
- hidden trust assumptions
- poor failure visibility

---

## 6. Lab 7 Application

Use the case study to strengthen three parts of your repo:

- `Agent Architecture` section in README
- safety checkpoint documentation
- episode log extension

If the lecture case study does not change your design decisions at all, your team did not extract enough from it.

---

*Guide for Lab 7 OpenClaw lessons.*

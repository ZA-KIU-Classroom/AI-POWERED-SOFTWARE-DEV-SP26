# LangGraph Guide

LangGraph is a graph-based orchestration framework.  
For Lab 7, the important concepts are:

- **node**
- **edge**
- **state**
- **conditional route**

Do not get lost in framework trivia.

---

## 1. The Core Model

### Node

A function that reads state and returns state updates.

### Edge

A connection that defines what runs next.

### State

The shared data object carried through the graph.

### Conditional edge

A routing function that decides the next node based on the current state.

---

## 2. Minimal Lab 7 Graph

The starter includes three nodes:

- `research`
- `write`
- `human_review`

And one route function:

- after `write`, either go to `human_review` or end

This is enough to teach the orchestration pattern without overloading the room.

---

## 3. Why This Matters

Many teams treat orchestration as invisible glue code.  
That makes debugging difficult.

A graph forces you to name:

- the stages
- the state transitions
- the branch conditions

That is why the starter exists.

---

## 4. How to Run the Starter

```bash
cd examples/langgraph-starter
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

You should see:
- the initial state
- the research update
- the write update
- the final route decision

---

## 5. What to Notice

When you run the starter, ask:

1. Which fields are read by `research`?
2. Which fields are written by `research`?
3. Which fields are read by `write`?
4. What condition triggers `human_review`?
5. Which of these map directly to our capstone?

If your team cannot answer these questions, rerun the starter and inspect the code.

---

## 6. LangGraph Is Not the Only Valid Path

You may keep your capstone in raw Python, FastAPI, or Next.js.

The Lab 7 requirement is not “migrate your app to LangGraph.”  
The requirement is “understand and implement orchestration concepts clearly.”

Use LangGraph when:
- the workflow is more than a few steps
- branching logic is growing
- durable state or checkpointing matters
- the graph representation improves readability

Keep raw orchestration when:
- the flow is small
- the graph would add overhead today
- your team still needs conceptual clarity more than framework depth

---

## 7. Optional LangSmith

If your team already uses LangSmith, add a trace for the mini-build.

This is optional for Lab 7.  
It becomes more useful later when you need observability evidence.

---

*Guide for Lab 7 LangGraph work.*

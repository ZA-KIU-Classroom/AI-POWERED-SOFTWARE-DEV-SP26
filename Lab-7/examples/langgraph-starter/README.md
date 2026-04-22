# LangGraph Starter

A minimal two-node orchestration proof for Lab 7.

This starter is intentionally small.  
It is for understanding **state**, **nodes**, and **conditional routing**.

## What it does

- receives an initial `AgentState`
- runs a `research` node
- runs a `write` node
- routes either to `human_review` or to end
- prints the final state

## Files

- `state.py` — typed state object
- `nodes.py` — node functions
- `graph.py` — graph assembly
- `main.py` — runnable entry point

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

## Teaching note

This starter does **not** depend on a live model call.  
The focus is the orchestration structure. Replace the placeholder logic with your real capstone logic after you understand the flow.

---

*Lab 7 example.*

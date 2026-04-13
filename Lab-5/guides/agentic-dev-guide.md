# Agentic Development Guide

**Using Cursor, VS Code with Continue, and Claude Code for Lab 5**
**CS-AI-2025 Spring 2026**

---

## The Rule

You are allowed and encouraged to use AI coding assistants during the sprint. The rule is simple:

> You must be able to explain every line of code in your prototype. If you cannot, slow down and read before you continue building.

The instructor may ask you to walk through your code at any point. "The AI wrote it" is not an explanation.

---

## Which Tool to Use

| Tool | Best for | Setup |
|---|---|---|
| **Cursor** | Full agentic sessions, large-scale code generation, understanding an unfamiliar codebase | Download at cursor.com, configure OpenRouter or Anthropic API key in settings |
| **VS Code + Continue** | Inline completions and chat within VS Code, works with any model | Install Continue extension, add OpenRouter key to config |
| **Claude Code (CLI)** | Terminal-based agentic coding, running tasks, editing files across your project | `npm install -g @anthropic-ai/claude-code`, requires Anthropic API key |

All three connect to models via OpenRouter or direct API keys. Use the same OpenRouter key from your `.env` file.

---

## Effective Prompting for This Sprint

The sprint goal is narrow: one working endpoint. Your prompts should be equally narrow.

### Bad prompt (too broad)

```
Build me a full AI-powered web application for summarising legal documents 
with user authentication, a dashboard, and a history of past summaries.
```

The agent will generate a lot of code you do not understand and cannot debug.

### Good prompt (scoped to today)

```
I am building a FastAPI endpoint at POST /api/summarise.

It should:
1. Accept a JSON body with a field called "text" (string, max 5000 chars)
2. Call the OpenRouter API using the openai Python SDK with model "google/gemini-2.0-flash-001"
3. Use this system prompt: "Summarise the following text in exactly three sentences."
4. Return a JSON response with fields: summary (str), model (str), input_tokens (int), output_tokens (int), latency_ms (int)
5. Log the same fields to stdout in a single line

The OPENROUTER_KEY is loaded from a .env file using python-dotenv.
I am using uv, not pip. The file is services/llm_service.py.

Write only the llm_service.py file. Do not generate the router or the main app yet.
```

### Principles for good agent prompts

1. **Scope to one file at a time.** Ask for `services/llm_service.py`, then `routers/ai_router.py`, then wire them together. Not all at once.

2. **Specify the exact interface.** Tell the agent what function signature you need, what it accepts, and what it returns. This prevents the agent from inventing its own structure that conflicts with the rest of your code.

3. **Name your constraints explicitly.** Package manager (`uv` not `pip`), framework version, environment variable names, file paths. The agent cannot infer these.

4. **Ask for one thing, verify, then ask for the next.** Agents make mistakes. A mistake in step 1 that you catch early costs 2 minutes. A mistake in step 1 that you discover in step 8 costs 30 minutes.

5. **Read the output before running it.** Spend 60 seconds reading what the agent generated. Look for imports you do not recognise, hardcoded values that should be environment variables, and missing error handling.

---

## When the Agent Gets It Wrong

Common agent mistakes on this type of task and how to fix them:

| Mistake | What to do |
|---|---|
| Agent uses `import openai` instead of the OpenAI SDK pattern | Tell it: "Use `from openai import OpenAI` and instantiate with `base_url` and `api_key`" |
| Agent hardcodes the API key as a string | Tell it: "The key must come from `os.environ['OPENROUTER_KEY']` loaded with `load_dotenv()`" |
| Agent returns the full OpenRouter response object instead of extracting fields | Tell it: "Extract `response.choices[0].message.content` for the text, `response.usage.prompt_tokens` for tokens" |
| Agent invents a database layer you did not ask for | Tell it: "Remove the database code. This endpoint is stateless. Respond only with the fields I specified." |
| Agent generates a frontend component instead of a backend route | Tell it: "I need the FastAPI route in `routers/ai_router.py`, not a React component." |

---

## Cursor-Specific Tips

- Use **Composer** (Cmd+I on Mac, Ctrl+I on Windows) for multi-file edits
- Use **Chat** (Cmd+L) for questions and explanations without editing files
- Use `@file` syntax to include specific files in context: `@services/llm_service.py`
- Use `@docs` to pull in documentation — `@docs FastAPI` adds FastAPI reference to context
- Always review the diff before accepting — click each changed file and read it

## Claude Code (CLI) Tips

- Start with `claude` in your project root — it indexes your codebase automatically
- Use `/add` to add specific files to context before asking questions
- Use `/clear` to reset context when starting a new task
- Good opening prompt: `"Describe what this codebase does so far"` before asking it to add anything

---

## The 10-Minute Rule

If you have been stuck on the same problem for 10 minutes — whether that is a bug, a concept, or an agent output you cannot understand — raise your hand. Do not burn the sprint on a single blocker. The instructor is here to unblock you.

---

*Agentic development guide for CS-AI-2025 Lab 5, Spring 2026.*

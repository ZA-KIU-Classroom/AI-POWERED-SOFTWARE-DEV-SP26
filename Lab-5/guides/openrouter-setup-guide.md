# OpenRouter Setup Guide

**For Lab 5, CS-AI-2025 Spring 2026**

---

## What is OpenRouter?

OpenRouter is a unified API gateway that gives you access to models from Google, Anthropic, OpenAI, Meta, and others through a single endpoint and a single API key. Your course uses a shared organisational account — your team representative received a key via email.

The key point: the API is identical to the OpenAI SDK. You change one line (`base_url`) and every model in the OpenRouter catalogue becomes available to you.

---

## Verifying Your Key

### Option 1: curl (fastest)

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.0-flash-001",
    "messages": [{"role": "user", "content": "Say: key works"}]
  }'
```

A successful response looks like:

```json
{
  "choices": [{"message": {"content": "key works"}}],
  "usage": {"prompt_tokens": 12, "completion_tokens": 3, "total_tokens": 15}
}
```

If you get `{"error": {"code": 401, ...}}`, your key is wrong. Check for trailing spaces or line breaks when you pasted it.

### Option 2: Python

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"],
)

response = client.chat.completions.create(
    model="google/gemini-2.0-flash-001",
    messages=[{"role": "user", "content": "Say: key works"}],
)

print(response.choices[0].message.content)
print(f"Tokens — in: {response.usage.prompt_tokens}, out: {response.usage.completion_tokens}")
```

### Option 3: TypeScript / Node

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_KEY,
});

const response = await client.chat.completions.create({
  model: "google/gemini-2.0-flash-001",
  messages: [{ role: "user", content: "Say: key works" }],
});

console.log(response.choices[0].message.content);
console.log(`Tokens — in: ${response.usage?.prompt_tokens}, out: ${response.usage?.completion_tokens}`);
```

---

## Storing Your Key Securely

Never put your key directly in your code. Store it in a `.env` file and load it at runtime.

**Python:**

```bash
# .env file (never commit this)
OPENROUTER_KEY=sk-or-v1-your-key-here
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ["OPENROUTER_KEY"]
```

**Next.js:**

```bash
# .env.local file (never commit this — Next.js ignores it by default)
OPENROUTER_KEY=sk-or-v1-your-key-here
```

```typescript
// Accessible server-side only (no NEXT_PUBLIC_ prefix)
const key = process.env.OPENROUTER_KEY;
```

**Verify `.gitignore` protects your secrets:**

```bash
cat .gitignore | grep -E "\.env|\.env\.local"
```

If nothing appears, add them:

```bash
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

---

## Recommended Models for the Sprint

Start with the cheapest model that meets your quality needs. Only upgrade if the output quality is not good enough for your use case.

| Model string | Best for | Cost |
|---|---|---|
| `google/gemini-2.0-flash-001` | First prototype, fast iteration | Very cheap |
| `google/gemini-2.5-pro` | Complex reasoning, long documents | Moderate |
| `anthropic/claude-sonnet-4-6` | Instruction following, code | Moderate |
| `openai/gpt-4o` | Comparison baseline | Moderate |

Check real-time pricing at [openrouter.ai/models](https://openrouter.ai/models).

---

## Fallback: Google AI Studio Direct

If OpenRouter is unavailable for any reason during the sprint:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content("Your prompt here")
print(response.text)
```

Your personal Google AI Studio key from Lab 1 still works for this. The OpenRouter SDK pattern is preferred — use AI Studio only as a fallback.

---

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Key wrong or missing | Check `.env` is in the right directory and `load_dotenv()` is called |
| `429 Too Many Requests` | Rate limit hit | Wait 10 seconds and retry, or switch to a cheaper model |
| `400 Bad Request` | Malformed request body | Check `messages` array format and `model` string spelling |
| `connection refused` | Network or proxy issue | Check internet connection, try `curl google.com` first |
| `usage is None` | Model did not return token counts | Add a null check: `if response.usage: ...` |

---

*Guide for CS-AI-2025 Lab 5, Spring 2026.*

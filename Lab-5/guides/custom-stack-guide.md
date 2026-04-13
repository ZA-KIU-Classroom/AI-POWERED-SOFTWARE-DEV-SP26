# Custom Stack Guide

**CS-AI-2025 Lab 5, Spring 2026 — For teams not using FastAPI or Next.js**

If your team chose a different stack in your Design Review, this guide explains how to apply the same sprint patterns regardless of framework.

---

## The Core Pattern Works Everywhere

The prototype sprint goal is one working AI-powered endpoint. The framework does not change the pattern:

1. Accept input (HTTP request, CLI argument, or stdin)
2. Build a prompt from that input
3. Call an AI model via OpenRouter or Google AI Studio
4. Return the output
5. Log the call with tokens and latency

Every example below does exactly this.

---

## Flask (Python)

```python
import os, time, json
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"],
)

@app.route("/api/generate", methods=["POST"])
def generate():
    body   = request.get_json()
    prompt = body.get("prompt", "")
    model  = body.get("model", "google/gemini-2.5-flash")

    start    = time.time()
    response = client.chat.completions.create(
        model    = model,
        messages = [{"role": "user", "content": prompt}],
    )
    latency = int((time.time() - start) * 1000)
    usage   = response.usage

    print(f"[COST] model={model} in={usage.prompt_tokens} out={usage.completion_tokens} latency={latency}ms")

    return jsonify({
        "content":       response.choices[0].message.content,
        "input_tokens":  usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "latency_ms":    latency,
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
```

---

## Node.js / Express (TypeScript)

```typescript
import express from "express";
import OpenAI  from "openai";

const app    = express();
const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey:  process.env.OPENROUTER_KEY,
});

app.use(express.json());

app.post("/api/generate", async (req, res) => {
  const { prompt, model = "google/gemini-2.5-flash" } = req.body;

  const start    = Date.now();
  const response = await client.chat.completions.create({
    model,
    messages: [{ role: "user", content: prompt }],
  });
  const latency = Date.now() - start;
  const usage   = response.usage;

  console.log(`[COST] model=${model} in=${usage?.prompt_tokens} out=${usage?.completion_tokens} latency=${latency}ms`);

  res.json({
    content:       response.choices[0].message.content,
    input_tokens:  usage?.prompt_tokens  ?? 0,
    output_tokens: usage?.completion_tokens ?? 0,
    latency_ms:    latency,
  });
});

app.listen(8000, () => console.log("Running on http://localhost:8000"));
```

---

## Google AI Studio Direct (No OpenRouter)

Use this if your OpenRouter key has stopped working during the sprint:

```python
import google.generativeai as genai
import os, time
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# gemini-2.5-flash: 10 RPM / 250 RPD on free tier
model = genai.GenerativeModel("gemini-2.5-flash")

start    = time.time()
response = model.generate_content("Your prompt here")
latency  = int((time.time() - start) * 1000)

print(response.text)
print(f"Latency: {latency}ms")
# Note: token counts available via response.usage_metadata
if response.usage_metadata:
    print(f"Tokens in={response.usage_metadata.prompt_token_count} out={response.usage_metadata.candidates_token_count}")
```

**Free tier model strings (April 2026):**
- `gemini-2.5-flash-lite` — 15 RPM / 1,000 RPD — fastest, best for prototyping
- `gemini-2.5-flash` — 10 RPM / 250 RPD — better quality, still free
- `gemini-2.5-pro` — 5 RPM / 100 RPD — most capable free model, use sparingly

**Deprecated — do not use:**
- `gemini-2.0-flash` — shut down June 1, 2026
- `gemini-2.0-flash-lite` — shut down June 1, 2026

---

## Using OpenRouter Free Models

No org credits needed. Any model with `:free` suffix is zero-cost:

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"],  # still need an account key, but no credits charged
)

response = client.chat.completions.create(
    model    = "meta-llama/llama-4-maverick:free",  # free, no credits
    messages = [{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

**Current reliable free models on OpenRouter (April 2026):**

| Model string | Best for |
|---|---|
| `meta-llama/llama-4-maverick:free` | General tasks, strong reasoning |
| `google/gemma-3-27b-it:free` | Instruction following, structured output |
| `deepseek/deepseek-r1:free` | Reasoning-heavy tasks, code |
| `openrouter/free` | Auto-selects best available free model |

Rate limits: 20 requests/minute, 200 requests/day per model. If you hit limits, rotate between models or use your org credits.

---

## The Cost Log is Still Required

No matter which stack you use, copy the cost logging pattern from `guides/cost-tracking-guide.md` and adapt it to your framework. The minimum is a `console.log` or `print` statement per call with: timestamp, model, purpose, input tokens, output tokens, latency, cost.

---

*Custom stack guide for CS-AI-2025 Lab 5, Spring 2026.*

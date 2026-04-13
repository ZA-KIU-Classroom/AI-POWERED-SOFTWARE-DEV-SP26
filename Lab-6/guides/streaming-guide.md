# Streaming Guide

**CS-AI-2025 Lab 6, Spring 2026**

This guide covers everything you need to add real-time streaming to your capstone endpoint. It is a complete reference — use it alongside the example code in `examples/`.

---

## What Streaming Is

When you call a model without streaming, your server waits for the entire response to be generated before it sends anything to the client. For a 300-word response, that is typically 2–5 seconds of silence.

With streaming, the model sends tokens as it generates them. Your server forwards each token immediately. The client renders them one by one. The user sees the first word in under 200ms.

The API change is one parameter: `stream=True` (Python) or `stream: true` (TypeScript).

---

## The Server-Sent Events Protocol

Streaming responses use Server-Sent Events (SSE). The rules are simple:

- Content-Type must be `text/event-stream`
- Each event is a line starting with `data: ` followed by a JSON payload
- Each event is terminated by `\n\n` (two newlines)
- The stream ends with the sentinel `data: [DONE]\n\n`

```
data: {"token": "Hello"}\n\n
data: {"token": " world"}\n\n
data: {"token": "!"}\n\n
data: [DONE]\n\n
```

Your client splits the incoming bytes on `\n`, looks for lines starting with `data: `, and processes each one.

---

## FastAPI Implementation

### The streaming route

```python
import json
import os
import time
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"],
)

DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "google/gemini-2.5-flash")


class StreamRequest(BaseModel):
    message:    str
    session_id: str
    system:     str | None = None


async def token_generator(messages: list, model: str, session_id: str):
    """Async generator that yields SSE-formatted token events."""
    stream_start = time.time()
    token_count  = 0

    try:
        response = client.chat.completions.create(
            model        = model,
            messages     = messages,
            stream       = True,
            stream_options = {"include_usage": True},
        )

        for chunk in response:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                token_count += 1
                yield f"data: {json.dumps({'token': delta})}\n\n"

            # Capture usage from the final chunk
            if chunk.usage:
                stream_end = time.time()
                latency_ms = int((stream_end - stream_start) * 1000)
                yield f"data: {json.dumps({'usage': {'input_tokens': chunk.usage.prompt_tokens, 'output_tokens': chunk.usage.completion_tokens, 'stream_start_ms': int(stream_start * 1000), 'stream_end_ms': int(stream_end * 1000), 'latency_ms': latency_ms}})}\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

    finally:
        yield "data: [DONE]\n\n"


@router.post("/ai/stream")
async def stream_chat(body: StreamRequest):
    from services.session_service import load_session, save_session_async

    messages = load_session(body.session_id)
    system   = body.system or "You are a helpful assistant."

    # Build the message list
    if not messages:
        messages = [{"role": "system", "content": system}]
    messages.append({"role": "user", "content": body.message})

    async def generate_and_save():
        full_response = ""
        async for chunk in token_generator(messages, DEFAULT_MODEL, body.session_id):
            if '"token"' in chunk:
                try:
                    data = json.loads(chunk.replace("data: ", "").strip())
                    full_response += data.get("token", "")
                except Exception:
                    pass
            yield chunk

        # Save the completed response to session history
        messages.append({"role": "assistant", "content": full_response})
        save_session_async(body.session_id, messages)

    return StreamingResponse(
        generate_and_save(),
        media_type="text/event-stream",
        headers={
            "Cache-Control":     "no-cache",
            "X-Accel-Buffering": "no",   # prevents nginx from buffering the stream
        },
    )
```

### Testing with curl

```bash
# The -N flag disables curl's own buffering so you see tokens arrive in real time
curl -N -X POST http://localhost:8000/api/ai/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Count from 1 to 5 slowly.", "session_id": "test-session-1"}'
```

---

## Next.js Implementation

### The streaming route

```typescript
// app/api/chat/stream/route.ts
import { NextRequest } from "next/server";
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey:  process.env.OPENROUTER_KEY ?? "",
});

const DEFAULT_MODEL = process.env.DEFAULT_MODEL ?? "google/gemini-2.5-flash";

export async function POST(req: NextRequest) {
  const { message, session_id, system } = await req.json() as {
    message:    string;
    session_id: string;
    system?:    string;
  };

  const { loadSession, saveSession } = await import("@/lib/session-store");
  const history = loadSession(session_id);
  const systemPrompt = system ?? "You are a helpful assistant.";

  if (history.length === 0) {
    history.push({ role: "system" as const, content: systemPrompt });
  }
  history.push({ role: "user" as const, content: message });

  const encoder = new TextEncoder();
  let fullResponse = "";
  const streamStart = Date.now();

  const stream = new ReadableStream({
    async start(controller) {
      try {
        const response = await client.chat.completions.create({
          model:          DEFAULT_MODEL,
          messages:       history,
          stream:         true,
          stream_options: { include_usage: true },
        });

        for await (const chunk of response) {
          const delta = chunk.choices[0]?.delta?.content;
          if (delta) {
            fullResponse += delta;
            controller.enqueue(
              encoder.encode(`data: ${JSON.stringify({ token: delta })}\n\n`)
            );
          }

          if (chunk.usage) {
            const streamEnd = Date.now();
            controller.enqueue(
              encoder.encode(
                `data: ${JSON.stringify({
                  usage: {
                    input_tokens:    chunk.usage.prompt_tokens,
                    output_tokens:   chunk.usage.completion_tokens,
                    stream_start_ms: streamStart,
                    stream_end_ms:   streamEnd,
                    latency_ms:      streamEnd - streamStart,
                  },
                })}\n\n`
              )
            );
          }
        }
      } catch (err) {
        controller.enqueue(
          encoder.encode(`data: ${JSON.stringify({ error: String(err) })}\n\n`)
        );
      } finally {
        // Save completed response to session
        history.push({ role: "assistant" as const, content: fullResponse });
        saveSession(session_id, history);

        controller.enqueue(encoder.encode("data: [DONE]\n\n"));
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type":    "text/event-stream",
      "Cache-Control":   "no-cache",
      "Connection":      "keep-alive",
    },
  });
}
```

### Frontend consumption pattern

```typescript
async function sendMessage(message: string, sessionId: string) {
  const controller = new AbortController();

  const response = await fetch("/api/chat/stream", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({ message, session_id: sessionId }),
    signal:  controller.signal,   // allows user to cancel mid-stream
  });

  const reader  = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const text  = decoder.decode(value);
    const lines = text.split("\n");

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const payload = line.slice(6).trim();
      if (payload === "[DONE]") return;

      try {
        const data = JSON.parse(payload);

        if (data.token) {
          // Append to your React state
          setResponse(prev => prev + data.token);
        }

        if (data.usage) {
          console.log("[STREAM COST]", data.usage);
          // Log to your episode log
        }

        if (data.error) {
          console.error("[STREAM ERROR]", data.error);
        }
      } catch {
        // Incomplete chunk — safe to ignore
      }
    }
  }
}
```

---

## Handling User Cancellation

If a user clicks a Stop button mid-stream, abort the fetch:

```typescript
const controller = new AbortController();

// Start stream
const response = await fetch("/api/chat/stream", {
  signal: controller.signal,
  // ...
});

// On Stop button click:
controller.abort();
// reader.read() will throw an AbortError — catch it gracefully
```

---

## Cost Logging for Streaming

Streaming costs the same as blocking calls — you are charged per token. What changes is when you receive the usage data. Capture it from the final chunk's `usage` field.

Add these fields to your episode log for streaming calls:

| Field | Description |
|---|---|
| `stream_start_ms` | Unix timestamp (ms) when the first chunk arrived |
| `stream_end_ms` | Unix timestamp (ms) when `[DONE]` was received |
| `latency_ms` | `stream_end_ms - stream_start_ms` |
| `was_cancelled` | `true` if the user aborted before `[DONE]` |
| `input_tokens` | From `chunk.usage.prompt_tokens` in the final chunk |
| `output_tokens` | From `chunk.usage.completion_tokens` in the final chunk |

---

## Common Mistakes

**Passing only the current message to the model:**
Every streaming call must include the full trimmed session history, not just the latest user message. A streaming endpoint that forgets the conversation is not an improvement over a blocking one.

**Not emitting `[DONE]`:**
The frontend `while(true)` loop runs forever if it never receives `[DONE]`. Always emit the sentinel in a `finally` block so it fires even if an error occurs mid-stream.

**Setting `NEXT_PUBLIC_` on your API key:**
Your key must stay server-side. The streaming route must be in `app/api/` and called from your own frontend with a relative URL. Never call OpenRouter directly from a browser.

---

*Streaming guide for CS-AI-2025 Lab 6, Spring 2026.*

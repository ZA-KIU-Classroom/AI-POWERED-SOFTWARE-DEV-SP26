/**
 * Streaming Chat Route — CS-AI-2025 Lab 6, Spring 2026
 *
 * POST /api/chat/stream
 *
 * Adds streaming to your existing capstone Next.js app.
 * Keep your Lab 5 route at /api/ai intact — this is a new route alongside it.
 *
 * Request body:
 *   { message: string, session_id: string, system?: string }
 *
 * Response: text/event-stream
 *   data: {"token": "..."}\n\n         — one per token
 *   data: {"usage": {...}}\n\n         — cost and latency summary
 *   data: [DONE]\n\n                   — end sentinel
 */

import { NextRequest } from "next/server";
import OpenAI from "openai";
import { loadSession, saveSession } from "@/lib/session-store";
import { logStreamEnd, logUserMessage, logError } from "@/lib/episode-logger";

// ---------------------------------------------------------------------------
// Client — server-side only, NEVER add NEXT_PUBLIC_ prefix to the key
// ---------------------------------------------------------------------------
const client = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey:  process.env.OPENROUTER_KEY ?? "",
});

const DEFAULT_MODEL = process.env.DEFAULT_MODEL ?? "google/gemini-2.5-flash";

// ---------------------------------------------------------------------------
// Route handler
// ---------------------------------------------------------------------------

export async function POST(req: NextRequest) {
  const body = await req.json() as {
    message:    string;
    session_id: string;
    system?:    string;
  };

  const { message, session_id, system } = body;

  if (!message || !session_id) {
    return new Response(
      JSON.stringify({ error: "message and session_id are required" }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  logUserMessage(session_id);

  const history     = loadSession(session_id);
  const systemText  = system ?? "You are a helpful assistant.";

  if (history.length === 0) {
    history.push({ role: "system" as const, content: systemText });
  }
  history.push({ role: "user" as const, content: message });

  const encoder      = new TextEncoder();
  const streamStart  = Date.now();
  let   fullResponse = "";
  let   inputTokens  = 0;
  let   outputTokens = 0;

  const stream = new ReadableStream({
    async start(controller) {
      const enqueue = (payload: object | string) => {
        const data = typeof payload === "string" ? payload : JSON.stringify(payload);
        controller.enqueue(encoder.encode(`data: ${data}\n\n`));
      };

      try {
        const response = await client.chat.completions.create({
          model:          DEFAULT_MODEL,
          messages:       history,
          stream:         true,
          stream_options: { include_usage: true },
        });

        for await (const chunk of response) {
          // Token delta
          const delta = chunk.choices[0]?.delta?.content;
          if (delta) {
            fullResponse += delta;
            enqueue({ token: delta });
          }

          // Usage (arrives in the final chunk)
          if (chunk.usage) {
            inputTokens  = chunk.usage.prompt_tokens     ?? 0;
            outputTokens = chunk.usage.completion_tokens ?? 0;
          }
        }

      } catch (err) {
        logError(session_id, err instanceof Error ? err : new Error(String(err)), "stream_generation");
        enqueue({ error: String(err) });

      } finally {
        const streamEnd = Date.now();

        // Emit usage summary before [DONE]
        enqueue({
          usage: {
            input_tokens:    inputTokens,
            output_tokens:   outputTokens,
            stream_start_ms: streamStart,
            stream_end_ms:   streamEnd,
            latency_ms:      streamEnd - streamStart,
          },
        });

        // Log to episode log
        logStreamEnd({
          session_id,
          model:           DEFAULT_MODEL,
          input_tokens:    inputTokens,
          output_tokens:   outputTokens,
          stream_start_ms: streamStart,
          stream_end_ms:   streamEnd,
        });

        // Save completed response to session history
        if (fullResponse) {
          history.push({ role: "assistant" as const, content: fullResponse });
          saveSession(session_id, history);
        }

        enqueue("[DONE]");
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type":  "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection":    "keep-alive",
    },
  });
}

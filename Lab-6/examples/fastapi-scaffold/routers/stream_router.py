"""
Streaming Router — CS-AI-2025 Lab 6, Spring 2026

Adds a streaming endpoint alongside the existing blocking endpoint from Lab 5.
Do NOT replace the Lab 5 blocking route — keep both. The streaming route is at
POST /api/ai/stream.
"""

import json
import os
import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

from services.session_service import load_session, save_session
from services.episode_logger import log_user_message, log_stream_end, log_error

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


@router.post("/ai/stream")
async def stream_chat(body: StreamRequest):
    """
    Streaming chat endpoint. Returns tokens as server-sent events.

    Request body:
        message:    The user's message text.
        session_id: A UUID identifying the conversation. Generate on the frontend
                    with crypto.randomUUID() and persist in sessionStorage.
        system:     Optional system prompt override.

    Response: text/event-stream
        Each event: data: {"token": "..."}\n\n
        Usage event: data: {"usage": {"input_tokens": N, ...}}\n\n
        End sentinel: data: [DONE]\n\n
    """
    log_user_message(body.session_id)

    messages = load_session(body.session_id)
    system   = body.system or "You are a helpful assistant."

    if not messages:
        messages = [{"role": "system", "content": system}]

    messages.append({"role": "user", "content": body.message})

    return StreamingResponse(
        _token_generator(body.session_id, messages, DEFAULT_MODEL),
        media_type="text/event-stream",
        headers={
            "Cache-Control":     "no-cache",
            "X-Accel-Buffering": "no",   # prevent nginx from buffering the stream
        },
    )


async def _token_generator(session_id: str, messages: list, model: str):
    """
    Async generator that yields SSE-formatted events.
    Saves the completed response to session history when the stream ends.
    """
    stream_start_ms = int(time.time() * 1000)
    full_response   = ""
    input_tokens    = 0
    output_tokens   = 0

    try:
        response = client.chat.completions.create(
            model          = model,
            messages       = messages,
            stream         = True,
            stream_options = {"include_usage": True},
        )

        for chunk in response:
            # Token delta
            if chunk.choices:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
                    yield f"data: {json.dumps({'token': delta})}\n\n"

            # Usage (arrives in the final chunk when stream_options is set)
            if chunk.usage:
                input_tokens  = chunk.usage.prompt_tokens     or 0
                output_tokens = chunk.usage.completion_tokens or 0

    except Exception as e:
        log_error(session_id, e, context="stream_generation")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

    finally:
        stream_end_ms = int(time.time() * 1000)

        # Emit the usage summary event before [DONE]
        yield f"data: {json.dumps({'usage': {'input_tokens': input_tokens, 'output_tokens': output_tokens, 'stream_start_ms': stream_start_ms, 'stream_end_ms': stream_end_ms, 'latency_ms': stream_end_ms - stream_start_ms}})}\n\n"

        # Log the episode
        log_stream_end(
            session_id      = session_id,
            model           = model,
            input_tokens    = input_tokens,
            output_tokens   = output_tokens,
            stream_start_ms = stream_start_ms,
            stream_end_ms   = stream_end_ms,
        )

        # Save assistant response to session history
        if full_response:
            messages.append({"role": "assistant", "content": full_response})
            save_session(session_id, messages)

        yield "data: [DONE]\n\n"

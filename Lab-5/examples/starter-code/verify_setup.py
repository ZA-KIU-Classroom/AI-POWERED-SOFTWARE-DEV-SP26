"""
verify_setup.py — CS-AI-2025 Lab 5, Spring 2026

Run this script at the start of the lab to confirm your AI connection
works before touching your capstone code.

Usage:
    uv run verify_setup.py
    # or: python verify_setup.py

Requires: OPENROUTER_KEY or GEMINI_API_KEY in .env
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()


def test_openrouter():
    """Test OpenRouter connection with a free model."""
    from openai import OpenAI

    key = os.environ.get("OPENROUTER_KEY", "")
    if not key:
        print("SKIP: OPENROUTER_KEY not set in .env")
        return False

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

    # Using a free model — no org credits consumed
    model = "google/gemini-2.5-flash"

    print(f"Testing OpenRouter with model: {model}")
    start = time.time()

    try:
        response = client.chat.completions.create(
            model    = model,
            messages = [{"role": "user", "content": "Reply with exactly: setup verified"}],
        )
        latency = int((time.time() - start) * 1000)
        content = response.choices[0].message.content
        usage   = response.usage

        print(f"  Response : {content}")
        print(f"  Latency  : {latency}ms")
        if usage:
            print(f"  Tokens   : in={usage.prompt_tokens} out={usage.completion_tokens}")
        print("  OpenRouter: OK\n")
        return True

    except Exception as e:
        print(f"  OpenRouter FAILED: {e}\n")
        return False


def test_google_ai_studio():
    """Test Google AI Studio direct connection (free tier)."""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        print("SKIP: GEMINI_API_KEY not set in .env")
        return False

    try:
        import google.generativeai as genai
    except ImportError:
        print("SKIP: google-generativeai not installed. Run: uv add google-generativeai")
        return False

    genai.configure(api_key=key)

    # Free tier models (April 2026):
    #   gemini-2.5-flash-lite  → 15 RPM / 1,000 RPD  ← fastest free option
    #   gemini-2.5-flash       → 10 RPM / 250 RPD
    #   gemini-2.5-pro         → 5 RPM  / 100 RPD
    #
    # DEPRECATED (do not use — shutdown June 1 2026):
    #   gemini-2.0-flash, gemini-2.0-flash-lite
    model_name = "gemini-2.5-flash-lite"

    print(f"Testing Google AI Studio with model: {model_name}")
    start = time.time()

    try:
        model    = genai.GenerativeModel(model_name)
        response = model.generate_content("Reply with exactly: setup verified")
        latency  = int((time.time() - start) * 1000)

        print(f"  Response : {response.text.strip()}")
        print(f"  Latency  : {latency}ms")
        if response.usage_metadata:
            meta = response.usage_metadata
            print(f"  Tokens   : in={meta.prompt_token_count} out={meta.candidates_token_count}")
        print("  Google AI Studio: OK\n")
        return True

    except Exception as e:
        print(f"  Google AI Studio FAILED: {e}\n")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("CS-AI-2025 Lab 5 — Setup Verification")
    print("=" * 50 + "\n")

    openrouter_ok = test_openrouter()
    gemini_ok     = test_google_ai_studio()

    print("=" * 50)
    if openrouter_ok or gemini_ok:
        print("RESULT: At least one connection is working.")
        print("You are ready to start the sprint.")
    else:
        print("RESULT: Neither connection worked.")
        print("Check your .env file and raise your hand for help.")
    print("=" * 50)

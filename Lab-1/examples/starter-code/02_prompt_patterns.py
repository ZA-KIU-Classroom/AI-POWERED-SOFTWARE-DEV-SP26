"""
CS-AI-2025 | Lab 1 | Exercise 2 — Prompt Pattern Explorer
Spring 2026 | Kutaisi International University

This script demonstrates the four core prompt engineering patterns:
  1. Zero-shot
  2. Few-shot
  3. Chain-of-thought
  4. System prompt

Each pattern is applied to the SAME underlying task so you can compare
the outputs side by side and build genuine intuition for when to use each one.

YOUR TASK:
After studying these four examples, modify the TOPIC and CUSTOM_TASK
variables below to apply all four patterns to a topic of YOUR choosing.
Record all results in your prompt log template.
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

try:
    import google.genai as genai
    from google.genai.types import GenerateContentConfig
except ImportError:
    print("ERROR: google-genai package not installed. Run: pip install google-genai")
    exit(1)


# ─── Configuration — MODIFY THIS SECTION ──────────────────────────────────────

MODEL = "gemini-3-flash-preview"

# Change these to apply the patterns to your own topic
TOPIC = "climate change"
CUSTOM_TASK = "classify whether each statement about climate change is a FACT, OPINION, or MYTH"


# ─── Helper Functions ──────────────────────────────────────────────────────────

def call_model(client, prompt, system_instruction=None, label=""):
    """
    Makes a single API call, prints the result with metrics.
    Returns the response object.
    """
    print(f"\n{'='*60}")
    print(f"PATTERN: {label}")
    print(f"{'='*60}")

    # Build config
    config = GenerateContentConfig(system_instruction=system_instruction) if system_instruction else None

    # Measure latency
    start = time.perf_counter()
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )
    latency_ms = (time.perf_counter() - start) * 1000

    usage = response.usage_metadata

    print(f"\nPROMPT SENT:")
    print("-" * 40)
    if system_instruction:
        print(f"[SYSTEM]\n{system_instruction}\n")
    print(f"[USER]\n{prompt}")
    print("-" * 40)

    print(f"\nRESPONSE:")
    print("-" * 40)
    print(response.text)
    print("-" * 40)

    print(f"\nMETRICS:")
    print(f"  Input tokens:   {usage.prompt_token_count}")
    print(f"  Output tokens:  {usage.candidates_token_count}")
    print(f"  Total tokens:   {usage.total_token_count}")
    print(f"  Latency:        {latency_ms:.0f} ms")

    return response


def pause(seconds=4):
    """
    Pauses between calls to stay within the free tier rate limit (15 RPM).
    At 15 RPM you can make 1 request every 4 seconds safely.
    """
    print(f"\n[Rate limit protection: waiting {seconds}s before next call...]")
    time.sleep(seconds)


# ─── Pattern Definitions ───────────────────────────────────────────────────────

def pattern_1_zero_shot(client):
    """
    Zero-shot: just the task, no examples, no special framing.
    The model uses its training to do what it thinks is correct.
    """
    prompt = f"""
What are the three most important things a first-year computer science student
should understand about {TOPIC}?
""".strip()

    return call_model(client, prompt, label="1 — Zero-Shot")


def pattern_2_few_shot(client):
    """
    Few-shot: we show the model examples of the input-output format
    before giving it the real task. This is especially useful when
    you need a specific output format or classification scheme.
    """
    prompt = f"""
{CUSTOM_TASK.capitalize()}.

Statement: "Scientists have reached overwhelming consensus on the cause."
Classification: FACT
Reason: This accurately reflects the state of scientific literature.

Statement: "The economic cost of action is too high."
Classification: OPINION
Reason: This involves value judgements about acceptable trade-offs, not objective facts.

Statement: "Cold winters prove that global warming is not happening."
Classification: MYTH
Reason: Local weather events are not evidence against long-term global temperature trends.

Statement: "Renewable energy cannot power an entire country reliably."
Classification:""".strip()

    return call_model(client, prompt, label="2 — Few-Shot")


def pattern_3_chain_of_thought(client):
    """
    Chain-of-thought: we ask the model to reason step by step before
    giving a conclusion. This produces more accurate results on tasks
    that require multi-step reasoning.
    """
    prompt = f"""
A policy-maker is deciding whether to fund research into {TOPIC}.
They have a budget of $10 million for the next 3 years.
Three options are on the table:

Option A: Fund academic research only ($10M to universities)
Option B: Fund applied industry R&D only ($10M to private companies)
Option C: Split 50/50 between academic and industry

Which option produces the most societal benefit?

Think through the trade-offs of each option step by step before giving your recommendation.
""".strip()

    return call_model(client, prompt, label="3 — Chain-of-Thought")


def pattern_4_system_prompt(client):
    """
    System prompts: a privileged, persistent instruction that shapes the
    model's persona, constraints, and output format. This is how you turn
    a general-purpose AI into a specific application.
    """
    system_instruction = f"""You are an expert science communicator specialising in {TOPIC}.
Your audience is intelligent but not technical — they read quality journalism but not academic papers.

When you respond:
- Lead with the single most important fact
- Use concrete analogies, never abstract jargon
- State your confidence level explicitly (High / Medium / Low)
- Keep every response under 120 words
- End with one question that invites the reader to think further"""

    user_prompt = f"What should I know about {TOPIC} that most people misunderstand?"

    return call_model(client, user_prompt, system_instruction=system_instruction, label="4 — System Prompt")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found. Check your .env file.")
        exit(1)

    client = genai.Client(api_key=api_key)

    print(f"\nCS-AI-2025 Lab 1 — Prompt Pattern Explorer")
    print(f"Topic: {TOPIC}")
    print(f"Model: {MODEL}")
    print(f"\nYou will see 4 API calls with different prompt patterns.")
    print(f"Study the differences in length, format, and quality of the responses.\n")

    # Run all four patterns with pauses to respect rate limits
    responses = []

    r1 = pattern_1_zero_shot(client)
    responses.append(("Zero-Shot", r1))
    pause()

    r2 = pattern_2_few_shot(client)
    responses.append(("Few-Shot", r2))
    pause()

    r3 = pattern_3_chain_of_thought(client)
    responses.append(("Chain-of-Thought", r3))
    pause()

    r4 = pattern_4_system_prompt(client)
    responses.append(("System Prompt", r4))

    # Summary table
    print(f"\n\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"{'Pattern':<25} {'Input':>8} {'Output':>8} {'Total':>8}")
    print("-" * 55)
    for label, r in responses:
        u = r.usage_metadata
        print(f"{label:<25} {u.prompt_token_count:>8} {u.candidates_token_count:>8} {u.total_token_count:>8}")

    total_tokens = sum(r.usage_metadata.total_token_count for _, r in responses)
    print("-" * 55)
    print(f"{'TOTAL':<25} {'':>8} {'':>8} {total_tokens:>8}")
    print(f"\nAll 4 calls completed at $0.00 (free tier).")

    print("\n" + "="*60)
    print("YOUR TASK — Now modify this script:")
    print("="*60)
    print("1. Change TOPIC to something from your own interests or capstone ideas")
    print("2. Update CUSTOM_TASK for the few-shot pattern")
    print("3. Run again and compare outputs")
    print("4. Record your results in: templates/prompt-log-template.md")
    print("5. This experiment is the foundation for Homework 1")
    print("\n✓ Exercise 2 complete. Proceed to Exercise 3.")
    print("  File: examples/starter-code/03_token_counter.py")


if __name__ == "__main__":
    main()

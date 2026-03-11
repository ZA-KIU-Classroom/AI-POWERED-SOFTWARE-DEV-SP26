"""
CS-AI-2025 | Lab 1 | Exercise 1 — Hello AI
Spring 2026 | Kutaisi International University

Your very first call to a language model API.

Before running this script:
1. Complete tools-setup.md
2. Create a .env file with your GEMINI_API_KEY
3. Activate your virtual environment: source venv/bin/activate
4. Run: python examples/starter-code/01_hello_gemini.py
"""

import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
# This MUST happen before importing google.genai in some configurations
load_dotenv()

try:
    import google.genai as genai
except ImportError:
    print("ERROR: google-genai package not installed.")
    print("Run: pip install google-genai")
    exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

MODEL = "gemini-3-flash-preview"

PROMPT = (
    "Tell me one fascinating, non-obvious thing about how large language models "
    "work internally — something that would genuinely surprise a computer science student "
    "who has never studied AI. Answer in exactly two sentences."
)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    # 1. Get the API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        print("Make sure you have a .env file with: GEMINI_API_KEY=your_key_here")
        print("See guides/gemini-setup-guide.md for instructions.")
        exit(1)

    # 2. Create the client
    print(f"Connecting to {MODEL}...")
    client = genai.Client(api_key=api_key)

    # 3. Count tokens before generating (optional but educational)
    token_count_result = client.models.count_tokens(
        model=MODEL,
        contents=PROMPT
    )
    print(f"\nPrompt: {PROMPT}")
    print(f"\nExpected input tokens: {token_count_result.total_tokens}")
    print("\nSending request...\n")

    # 4. Make the API call and measure latency
    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=MODEL,
        contents=PROMPT
    )

    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000

    # 5. Display the response
    print("─" * 60)
    print("RESPONSE:")
    print("─" * 60)
    print(response.text)
    print("─" * 60)

    # 6. Display usage metrics
    usage = response.usage_metadata
    print("\nTOKEN USAGE:")
    print(f"  Input tokens:  {usage.prompt_token_count}")
    print(f"  Output tokens: {usage.candidates_token_count}")
    print(f"  Total tokens:  {usage.total_token_count}")

    print(f"\nLATENCY:")
    print(f"  Total time: {latency_ms:.0f} ms")

    print(f"\nCOST ESTIMATE:")
    print(f"  Free tier:  $0.00 (you are not being charged)")
    # Reference calculation for awareness
    input_cost  = (usage.prompt_token_count    / 1_000_000) * 0.10
    output_cost = (usage.candidates_token_count / 1_000_000) * 0.40
    paid_cost   = input_cost + output_cost
    print(f"  Paid tier equivalent (gemini-3-flash-preview): ${paid_cost:.6f}")

    print("\n✓ Exercise 1 complete. Proceed to Exercise 2.")
    print("  File: examples/starter-code/02_prompt_patterns.py")


if __name__ == "__main__":
    main()

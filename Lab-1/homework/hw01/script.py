import os
import time
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

MODELS = [
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite-preview",
]

PROMPT = "Explain one important difference between supervised learning and unsupervised learning in simple terms."

PRICE_INPUT_PER_MILLION = 0.10
PRICE_OUTPUT_PER_MILLION = 0.40

def compute_cost(input_tokens, output_tokens):
    input_cost = (input_tokens / 1_000_000) * PRICE_INPUT_PER_MILLION
    output_cost = (output_tokens / 1_000_000) * PRICE_OUTPUT_PER_MILLION
    return input_cost + output_cost

def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    results = []

    for i, model in enumerate(MODELS, start=1):
        print(f"\n--- Call {i}: {model} ---")

        token_count = client.models.count_tokens(
            model=model,
            contents=PROMPT
        )
        print(f"Estimated input tokens: {token_count.total_tokens}")

        start = time.perf_counter()
        response = client.models.generate_content(
            model=model,
            contents=PROMPT
        )
        latency_ms = (time.perf_counter() - start) * 1000

        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count
        cost = compute_cost(input_tokens, output_tokens)

        print("Response text:")
        print(response.text)
        print()
        print(f"Input tokens:  {input_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total tokens:  {total_tokens}")
        print(f"Latency (ms):  {latency_ms:.0f}")
        print(f"Paid-tier cost equivalent: ${cost:.8f}")

        results.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "latency_ms": round(latency_ms),
            "cost": cost
        })

    print("\n| Call | Model | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Cost (paid equiv.) |")
    print("|---|---|---:|---:|---:|---:|---:|")
    for idx, r in enumerate(results, start=1):
        print(f"| {idx} | {r['model']} | {r['input_tokens']} | {r['output_tokens']} | {r['total_tokens']} | {r['latency_ms']} | ${r['cost']:.8f} |")

if __name__ == "__main__":
    main()
# Token and Cost Guide

**Understanding how AI pricing works and why it matters from day one.**

---

## What Is a Token?

A token is the basic unit of text that language models process. It is not a word, a character, or a byte — it sits somewhere between these. The most common tokenization scheme (BPE, or Byte-Pair Encoding) breaks text into sub-word units based on frequency patterns in training data.

**Rough approximations for English text:**
- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words ≈ one short paragraph
- 1,000 tokens ≈ 750 words ≈ a medium-length blog post

**Examples (approximate):**

| Text | Tokens |
|------|--------|
| `Hello` | 1 |
| `Hello, world!` | 4 |
| `Tokenization is fascinating` | 4 |
| `supercalifragilisticexpialidocious` | 7 |
| `def calculate_fibonacci(n):` | 7 |
| One full paragraph (100 words) | ~130 |
| One page of text (500 words) | ~650 |

**Why "approximate"?** The exact tokenization depends on the model's tokenizer. GPT models and Gemini models use different tokenizers and will produce slightly different token counts for the same text. The differences are small but matter at scale.

---

## Input vs. Output Tokens

All API providers charge separately for input tokens and output tokens, and output tokens are almost always more expensive.

**Input tokens** are everything you send: your system prompt, your user prompt, your few-shot examples, and any conversation history.

**Output tokens** are the model's response.

If you are building a chatbot that maintains conversation history, your input tokens grow with every turn. A conversation with 20 turns and 200 tokens per turn means turn 20 has 4,000+ tokens in the input from history alone — before you even count the current user message. This is why memory management and context window strategies matter (you will learn these in Week 7).

---

## Pricing for the Models in This Course

### Gemini Free Tier (Lab 1)

| Model | Input | Output | Notes |
|-------|-------|--------|-------|
| `gemini-3-flash-preview` (free tier) | $0.00 | $0.00 | Up to 1,500 req/day |
| `gemini-3.1-flash-lite-preview` (free tier) | $0.00 | $0.00 | Reasoning traces included |

### Paid Tier Reference (via OpenRouter — Lab 2 onwards)

These are approximate prices as of March 2026. Prices change frequently.

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|-----------------------|------------------------|
| `google/gemini-3-flash-preview` | $0.10 | $0.40 |
| `google/gemini-3.1-flash` | $0.10 | $0.40 |
| `google/gemini-3.1-pro` | $1.25 | $5.00 |
| `anthropic/claude-opus-4-6` | $15.00 | $75.00 |
| `openai/gpt-5.2` | $10.00 | $30.00 |
| `openai/gpt-4.1-mini` | $0.40 | $1.60 |

**Reading this table:** Claude Opus 4.6 at $75/M output tokens is 250x more expensive per output token than Gemini 3 Flash at $0.40/M. This does not mean Claude is wrong to use — it means you need to understand *when* the quality difference justifies the cost. This cost-performance reasoning is central to the course.

---

## Calculating Your Cost

**Formula:**

```
Cost = (input_tokens / 1,000,000 × input_price) + (output_tokens / 1,000,000 × output_price)
```

**Example calculation:**

You send a prompt with 150 input tokens and receive 300 output tokens using `gemini-3-flash-preview` on the paid tier.

```
Cost = (150 / 1,000,000 × $0.10) + (300 / 1,000,000 × $0.40)
Cost = $0.0000113 + $0.000090
Cost = ~$0.0001 (one-tenth of a cent)
```

That is extremely cheap per call. The costs become significant at scale:
- 10,000 such calls per day: ~$1.00/day
- 100,000 calls per day: ~$10.00/day
- 1,000,000 calls per day: ~$100.00/day — at which point optimization matters enormously

This is why cost-awareness from day one is essential.

---

## How to Count Tokens in Code

### Using the Gemini SDK

```python
import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Method 1: Count tokens before generating (useful for budget enforcement)
my_prompt = "Explain what a large language model is in simple terms."

token_count = client.models.count_tokens(
    model="gemini-3-flash-preview",
    contents=my_prompt
)
print(f"Input token count: {token_count.total_tokens}")

# Method 2: Read token usage from the response after generation
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=my_prompt
)

print(f"Input tokens used:  {response.usage_metadata.prompt_token_count}")
print(f"Output tokens used: {response.usage_metadata.candidates_token_count}")
print(f"Total tokens:       {response.usage_metadata.total_token_count}")
```

### Computing cost programmatically

```python
def compute_cost(input_tokens, output_tokens, model="gemini-3-flash-preview"):
    """
    Returns estimated cost in USD.
    Prices are approximate as of March 2026.
    Always verify against the official pricing page.
    """
    pricing = {
        "gemini-3-flash-preview": {"input": 0.10, "output": 0.40},
        "gemini-3.1-flash":  {"input": 0.10,  "output": 0.40},
        "gemini-3.1-pro":    {"input": 1.25,  "output": 5.00},
    }
    if model not in pricing:
        return None  # Free tier or unsupported model
    
    rates = pricing[model]
    input_cost  = (input_tokens  / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    return input_cost + output_cost

cost = compute_cost(150, 300, "gemini-3-flash-preview")
print(f"Estimated cost: ${cost:.6f}")
```

---

## Latency: The Other Dimension

Cost is only one axis of model performance. Latency is the other.

**Time to First Token (TTFT)** — how long before the first character of the response appears. Critical for streaming UIs.

**Total Latency** — how long before the full response is complete. What you typically measure in a non-streaming call.

**Tokens per Second (TPS)** — the generation speed once the model starts. Higher is better for long outputs.

### Measuring latency in Python

```python
import time

start = time.perf_counter()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Write a haiku about machine learning."
)
end = time.perf_counter()

latency_ms = (end - start) * 1000
output_tokens = response.usage_metadata.candidates_token_count
tokens_per_second = output_tokens / (end - start)

print(f"Total latency:     {latency_ms:.0f} ms")
print(f"Output tokens:     {output_tokens}")
print(f"Tokens per second: {tokens_per_second:.1f}")
```

### Typical latency ranges (March 2026)

| Model | Typical Latency (200-token response) |
|-------|--------------------------------------|
| Gemini 3 Flash | 800 ms – 1,500 ms |
| Gemini 3.1 Flash | 600 ms – 1,200 ms |
| Gemini 3.1 Pro | 2,000 ms – 5,000 ms |
| Claude Opus 4.6 | 3,000 ms – 8,000 ms |
| GPT-5.2 | 2,000 ms – 6,000 ms |

These are rough ranges and vary significantly with load, network conditions, and output length.

---

## Cost Discipline in This Course

The syllabus requires that all submissions include cost logs. Here is what this means in practice:

**Every API call you make should be logged.** Use the prompt log template.

**Every homework submission includes a cost summary.** Use the cost tracker template.

**Set personal budgets.** Before running experiments, estimate how many calls you plan to make and at what average token count. This forces intentionality.

**Never run unbounded loops against a paid API.** Always add a stop condition. Always test with free tier or a small loop count before scaling up.

The habit of cost-awareness you build in Week 1 will directly impact the quality of your work in Weeks 10 and 11 (optimization and evaluation), where you will be measured on your ability to reduce cost per interaction.

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Tokens | 1 token ≈ 4 characters ≈ 0.75 words |
| Input vs output | Output tokens cost more — minimize verbose prompts |
| Measurement | Use `usage_metadata` from the response object |
| Cost formula | `(input_tokens / 1M × input_price) + (output_tokens / 1M × output_price)` |
| Latency | Measure with `time.perf_counter()` around the API call |
| Discipline | Log every call; never run an unbounded loop against a paid API |

---

*Token and Cost Guide for CS-AI-2025 Lab 1, Spring 2026.*  
*Reference prices should be verified at [openrouter.ai/models](https://openrouter.ai/models) before any production cost estimation.*

# Prompt Engineering 101

**The four prompt patterns that every AI application developer must master.**

This guide covers the prompting fundamentals you need for Lab 1 and Homework 1. These patterns are not tricks or workarounds — they are the primary vocabulary through which you communicate intent to language models. Every AI application you build in this course, and in your career, will use combinations of these patterns.

---

## Why Prompt Engineering Matters

The same model, asked the same question in different ways, produces radically different outputs in terms of quality, format, accuracy, and usefulness. Prompt engineering is the discipline of understanding *why* these differences occur and *how* to structure prompts intentionally.

In 2026, frontier models like Claude Opus 4.6, Gemini 3.1, and GPT-5.2 are significantly more capable than their predecessors, but the fundamental patterns for prompting them remain the same as those established in 2022–2023. The patterns work because they exploit the way transformer models process context.

---

## Pattern 1: Zero-Shot Prompting

**What it is:** You give the model a task with no examples, no context, no special structure — just the task itself.

**When to use it:** When the task is common and well-represented in the model's training data. When you want to test baseline model capability. When simplicity matters and the output quality is already good enough.

**When it fails:** Complex, unusual, or multi-step tasks. Tasks that require specific output formats. Tasks where "correct" depends on a definition the model does not have.

### Example

```python
prompt = "Summarize the key differences between a REST API and a GraphQL API."
```

The model knows what REST and GraphQL are from its training data, can produce a useful summary, and there is no need to demonstrate the format you want.

### When to reach for a different pattern

If you run a zero-shot prompt and the output is wrong, vague, or formatted in a way you did not want — do not repeat the same prompt. Move to few-shot or chain-of-thought.

---

## Pattern 2: Few-Shot Prompting

**What it is:** You provide the model with two to five examples of the input-output pattern you want, then give it the real input.

**When to use it:** When the task has a specific format or style. When zero-shot produces the wrong output structure. When you want consistent, reproducible formatting across many inputs.

**How it works:** The examples become part of the context. The model identifies the pattern from the examples and applies it to the new input. This is sometimes called "in-context learning."

### Example

```python
prompt = """
Classify the sentiment of customer reviews as POSITIVE, NEGATIVE, or NEUTRAL.

Review: "The product arrived on time and works exactly as described."
Sentiment: POSITIVE

Review: "Terrible quality. Broke after two uses. Complete waste of money."
Sentiment: NEGATIVE

Review: "It's fine. Does what it says. Nothing special."
Sentiment: NEUTRAL

Review: "Absolutely love this! Best purchase I've made all year."
Sentiment:"""
```

The model has seen three examples and will continue the pattern, outputting `POSITIVE`.

### Key considerations for few-shot prompts

**Example quality matters more than quantity.** Two excellent examples outperform five mediocre ones. Each example should clearly demonstrate the pattern.

**Order matters slightly.** The last example before the target input has the strongest influence. Put your most representative example last.

**Balance your examples.** If you are doing classification, include examples of every class. Models are sensitive to the distribution of examples in your prompt.

---

## Pattern 3: Chain-of-Thought (CoT) Prompting

**What it is:** You instruct the model to reason step-by-step before giving its final answer, or you demonstrate step-by-step reasoning in your examples.

**When to use it:** Math, logic, or multi-step reasoning tasks. Any problem where getting the *reasoning* right is necessary to get the *answer* right. When you need to audit the model's reasoning, not just its conclusion.

**Why it works:** When the model is forced to write out intermediate steps, those steps become part of its context window. It effectively conditions itself on its own correct reasoning. This is why "think step by step" is one of the most well-studied prompting techniques.

### Example: Zero-shot CoT trigger phrase

```python
prompt = """
A train leaves Station A at 09:00 travelling at 80 km/h. 
Another train leaves Station B at 10:00 travelling at 120 km/h.
The distance between Station A and Station B is 300 km.
They are travelling towards each other. At what time do they meet?

Think step by step before giving your final answer.
"""
```

The phrase "Think step by step before giving your final answer" is the trigger. The model will now write out the intermediate calculations before answering, making the reasoning auditable and typically more accurate.

### Example: Few-shot CoT (demonstrating the reasoning pattern)

```python
prompt = """
Solve these word problems step by step.

Problem: A recipe needs 2.5 cups of flour for 12 cookies. 
How much flour for 30 cookies?
Reasoning: 30 cookies ÷ 12 cookies = 2.5 times the recipe. 
2.5 cups × 2.5 = 6.25 cups.
Answer: 6.25 cups

Problem: A developer earns $85/hour and works 7.5 hours on Monday and 4.5 hours on Tuesday.
What is her total earnings?
Reasoning: Monday: 7.5 hours × $85 = $637.50. Tuesday: 4.5 hours × $85 = $382.50.
Total: $637.50 + $382.50 = $1,020.00.
Answer: $1,020.00

Problem: A dataset has 840 rows. 15% are missing the target label. 
How many complete rows remain?
Reasoning:"""
```

### CoT and reasoning models

Gemini 3 Flash Thinking and Claude Opus 4.6 with extended thinking are *reasoning models* — they perform chain-of-thought internally before generating a response. When you use these models, you often get the reasoning trace back as part of the response. This is the same principle as CoT prompting, automated at the model level.

---

## Pattern 4: System Prompts

**What it is:** A separate, privileged message that sets the model's persona, constraints, output format, and operating context before any user input is processed.

**When to use it:** Almost always, in application development. System prompts are the primary mechanism for turning a general-purpose AI into a specific application. Your capstone project will have a carefully engineered system prompt.

**Why it is different from a user prompt:** Most model providers treat system prompts as higher-authority instructions. They establish the context within which all user messages are interpreted. A well-crafted system prompt can define output format, language style, domain knowledge focus, refusal policies, and response length.

### Example

```python
import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import GenerateContentConfig

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = """You are a senior Python code reviewer at a software company.
When a developer shows you code, you:
1. First summarize what the code does in one sentence
2. Identify up to three specific improvements with brief explanations
3. Rate the code quality as GOOD, NEEDS WORK, or CRITICAL ISSUES
4. Keep your response under 200 words total

You are direct, specific, and constructive. You never pad your response."""

user_code = """
def get_data(url):
    import requests
    r = requests.get(url)
    data = r.json()
    return data
"""

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=user_code,
    config=GenerateContentConfig(
        system_instruction=system_instruction
    )
)

print(response.text)
```

### Key principles for system prompts

**Be specific about format.** Vague instructions like "be helpful" are far less effective than "respond in bullet points" or "keep responses under 150 words."

**Define what the model IS and what it does NOT do.** Positive and negative constraints together are more robust than either alone.

**Test edge cases.** Your system prompt will be tested by users doing unexpected things. Test it yourself before deploying.

**Keep it tight.** Every token in your system prompt costs money on every call. Ruthlessly edit out anything that is not contributing to better outputs.

---

## Combining Patterns

Real applications combine these patterns. A production prompt might have:
- A system prompt defining the application context (Pattern 4)
- A few-shot block demonstrating the output format (Pattern 2)
- A trigger phrase asking the model to reason before answering (Pattern 3)

This combination is standard practice in well-engineered AI applications.

---

## Quick Reference

| Pattern | Key Phrase / Structure | Best For |
|---------|----------------------|----------|
| Zero-shot | Just the task | Common, straightforward tasks |
| Few-shot | Examples → Task | Specific formats, consistent output |
| Chain-of-Thought | "Think step by step" | Reasoning, math, multi-step logic |
| System Prompt | Separate system field | Application context, personas, constraints |

---

## What to Practise in Lab 1

During Exercise 2, apply each of these four patterns to the same base task (a topic of your choosing). Compare the outputs. Note in your prompt log which pattern produced the best result and why.

This comparison exercise — same task, different patterns — is the fastest way to develop intuition for which pattern to reach for in a given situation.

---

*Prompt Engineering 101 for CS-AI-2025 Lab 1, Spring 2026.*  
*For deeper reading: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022).*

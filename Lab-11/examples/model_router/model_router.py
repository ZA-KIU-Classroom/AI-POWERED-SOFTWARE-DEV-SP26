"""
examples/model_router/model_router.py

Task-based model routing — routes requests to different models
based on the complexity of the task. This is optional strong-evidence
work for Lab 11. Integrate it after the fallback chain is working.

The routing table maps task complexity tiers to specific models.
Simple tasks go to cheap, fast models. Complex tasks go to capable,
more expensive models.

Usage:
    python examples/model_router/model_router.py
"""

import logging
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── Task complexity tiers ──────────────────────────────────────────────────────

class TaskComplexity(Enum):
    SIMPLE   = "simple"    # binary questions, classification, yes/no
    STANDARD = "standard"  # summarisation, Q&A, explanation
    COMPLEX  = "complex"   # multi-step reasoning, code review, debugging


# ── Routing table ─────────────────────────────────────────────────────────────
# Change these values to route different task tiers to different models.
# All values are read from environment so you can adjust per deployment.

ROUTING_TABLE: dict[TaskComplexity, str] = {
    TaskComplexity.SIMPLE:   os.environ.get("SIMPLE_MODEL",   "google/gemini-3-flash"),
    TaskComplexity.STANDARD: os.environ.get("PRIMARY_MODEL",  "anthropic/claude-sonnet-4-6"),
    TaskComplexity.COMPLEX:  os.environ.get("PRIMARY_MODEL",  "anthropic/claude-sonnet-4-6"),
}

# Fallback for each tier — activated if the routed model fails
TIER_FALLBACKS: dict[TaskComplexity, str] = {
    TaskComplexity.SIMPLE:   os.environ.get("PRIMARY_MODEL",  "anthropic/claude-sonnet-4-6"),
    TaskComplexity.STANDARD: os.environ.get("SECONDARY_MODEL","google/gemini-3-flash"),
    TaskComplexity.COMPLEX:  os.environ.get("SECONDARY_MODEL","google/gemini-3-flash"),
}

# ── Task classifier ───────────────────────────────────────────────────────────

# Keyword-based heuristics for classifying task complexity.
# Replace with a trained classifier once you have labelled data from
# your episode log.

SIMPLE_SIGNALS = [
    "yes or no",
    "true or false",
    "is this",
    "classify",
    "which category",
    "tag this",
    "correct or incorrect",
    "does this contain",
]

COMPLEX_SIGNALS = [
    "debug",
    "explain why",
    "what is wrong with",
    "analyse",
    "compare and contrast",
    "design a",
    "step by step",
    "reasoning",
    "code review",
    "refactor",
    "architecture",
    "multi-step",
]


def classify_task(user_message: str) -> TaskComplexity:
    """
    Classify a user message into a complexity tier.

    This is a keyword heuristic — good enough for a demo and Lab 11.
    For production: train a small classifier on your episode log data
    once you have 500+ labelled examples.

    Returns:
        TaskComplexity enum value
    """
    msg_lower = user_message.lower()

    # Check simple signals first — short-circuit on match
    for signal in SIMPLE_SIGNALS:
        if signal in msg_lower:
            return TaskComplexity.SIMPLE

    # Check complex signals
    for signal in COMPLEX_SIGNALS:
        if signal in msg_lower:
            return TaskComplexity.COMPLEX

    # Message length as a weak signal — longer questions tend to be more complex
    word_count = len(user_message.split())
    if word_count > 80:
        return TaskComplexity.COMPLEX
    if word_count < 10:
        return TaskComplexity.SIMPLE

    return TaskComplexity.STANDARD


def route_request(user_message: str) -> dict:
    """
    Classify the task and return routing metadata.

    Returns:
        {
            "complexity":     str  — "simple" | "standard" | "complex"
            "primary_model":  str  — model to try first for this tier
            "fallback_model": str  — model to try if primary fails
        }
    """
    complexity    = classify_task(user_message)
    primary_model = ROUTING_TABLE[complexity]
    fallback_model = TIER_FALLBACKS[complexity]

    logger.info(
        "Task routed: complexity=%s primary=%s fallback=%s",
        complexity.value, primary_model, fallback_model,
    )

    return {
        "complexity":     complexity.value,
        "primary_model":  primary_model,
        "fallback_model": fallback_model,
    }


# ── Integration with fallback chain ──────────────────────────────────────────

"""
To use task-based routing with the fallback chain, update your chat endpoint:

    from backend.llm_client import chat_with_fallback
    from backend.model_router import route_request, ROUTING_TABLE, TaskComplexity
    import os

    @app.post("/api/ai/chat")
    async def chat(request: ChatRequest):
        # Classify the task
        routing = route_request(request.messages[-1]["content"])

        # Build a per-request fallback chain based on the tier
        complexity  = TaskComplexity(routing["complexity"])
        chain = [
            routing["primary_model"],
            routing["fallback_model"],
            os.environ.get("OSS_FALLBACK", "qwen/qwen-3.5-32b"),
        ]

        # Use the standard fallback chain with the routed chain
        result = chat_with_fallback(
            messages    = request.messages,
            max_tokens  = 1024,
        )

        log_episode(
            ...
            model_used   = result["model_used"],
            task_complexity = routing["complexity"],  # NEW field for analysis
            fallback_used   = result["fallback_used"],
        )

        return {
            "content":        result["content"],
            "model_used":     result["model_used"],
            "task_complexity": routing["complexity"],
        }
"""

# ── Standalone test ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_cases = [
        ("Is this message spam? 'Buy cheap watches now!!!'", TaskComplexity.SIMPLE),
        ("Summarise the key points from this paragraph.", TaskComplexity.STANDARD),
        ("Debug this Python code and explain why the recursion fails.", TaskComplexity.COMPLEX),
        ("Hello, how are you?", TaskComplexity.SIMPLE),
        ("Compare and contrast RAG with long-context models for document Q&A.", TaskComplexity.COMPLEX),
        ("What is the capital of Georgia?", TaskComplexity.SIMPLE),
    ]

    print("Task Router — Classification Test\n")
    print(f"{'Message':<60} {'Expected':<12} {'Got':<12} {'Match'}")
    print("-" * 90)

    correct = 0
    for msg, expected in test_cases:
        result      = classify_task(msg)
        match       = result == expected
        correct    += int(match)
        marker      = "OK" if match else "FAIL"
        short_msg   = msg[:57] + "..." if len(msg) > 60 else msg
        print(f"{short_msg:<60} {expected.value:<12} {result.value:<12} {marker}")

    print(f"\nAccuracy: {correct}/{len(test_cases)}")
    print("\nRouting table:")
    for tier, model in ROUTING_TABLE.items():
        print(f"  {tier.value:<10} -> {model}")

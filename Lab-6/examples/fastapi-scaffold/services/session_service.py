"""
Session Service — CS-AI-2025 Lab 6, Spring 2026

In-memory conversation state management with sliding window trimming.
Suitable for Lab 6. Replace the storage backend with Redis in Week 12
without changing the interface.
"""

# ─── In-process store ────────────────────────────────────────────────────────
# Maps session_id (str) to a list of message dicts.
# This lives in process memory — lost on server restart.
_sessions: dict[str, list] = {}

# Keep system prompt(s) plus the last MAX_TURNS * 2 messages (user + assistant).
# At an average of 100 tokens per message, 20 turns ≈ 4,000 tokens of history.
MAX_TURNS = 20


# ─── Public interface ─────────────────────────────────────────────────────────

def load_session(session_id: str) -> list:
    """
    Return a copy of the message history for this session.
    Returns an empty list if the session does not exist.
    """
    return list(_sessions.get(session_id, []))


def save_session(session_id: str, messages: list) -> None:
    """
    Save the message history, applying the sliding window trim.
    The system prompt is always preserved at position 0.
    """
    _sessions[session_id] = _trim(messages)


def delete_session(session_id: str) -> None:
    """
    Delete all history for a session.
    Call this when a user requests data deletion.
    Required for GDPR compliance — expose via DELETE /api/session/{session_id}.
    """
    _sessions.pop(session_id, None)


def list_sessions() -> list[str]:
    """Return all active session IDs (for debugging only — not for user-facing APIs)."""
    return list(_sessions.keys())


def session_length(session_id: str) -> int:
    """Return the number of messages in a session."""
    return len(_sessions.get(session_id, []))


# ─── Internal helpers ─────────────────────────────────────────────────────────

def _trim(messages: list) -> list:
    """
    Sliding window trim.

    Keeps:
    - All system-role messages (usually just one — the system prompt)
    - The most recent MAX_TURNS * 2 non-system messages

    This prevents the context window from growing unboundedly over a long session.
    The model will never see more than ~(MAX_TURNS * avg_message_tokens) tokens
    of history at any one time.
    """
    system_messages = [m for m in messages if m.get("role") == "system"]
    non_system      = [m for m in messages if m.get("role") != "system"]

    max_non_system = MAX_TURNS * 2   # each turn = 1 user + 1 assistant message

    if len(non_system) <= max_non_system:
        return system_messages + non_system

    # Keep only the most recent messages
    return system_messages + non_system[-max_non_system:]

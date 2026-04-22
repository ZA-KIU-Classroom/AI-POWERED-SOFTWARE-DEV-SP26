from typing import TypedDict


class AgentState(TypedDict, total=False):
    session_id: str
    user_request: str
    messages: list[dict]
    current_step: str
    approval_required: bool
    approved: bool | None
    retry_count: int
    timeout_ms: int
    last_error: str | None
    research_notes: str | None
    final_response: str | None

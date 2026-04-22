from typing import TypedDict


class AgentState(TypedDict, total=False):
    session_id: str
    user_request: str
    current_step: str
    research_notes: str
    draft: str
    approval_required: bool
    approved: bool | None
    retry_count: int
    timeout_ms: int
    last_error: str | None
    final_response: str | None

from state import AgentState


def research_node(state: AgentState) -> AgentState:
    request = state.get("user_request", "")
    notes = (
        f"Research notes for request: {request}. "
        "Replace this placeholder with retrieval or analysis logic from your capstone."
    )

    return {
        "current_step": "research_complete",
        "research_notes": notes,
    }


def write_node(state: AgentState) -> AgentState:
    notes = state.get("research_notes", "")
    request = state.get("user_request", "")

    draft = (
        f"Draft response for '{request}'. "
        f"Based on notes: {notes}"
    )

    # Simple teaching rule:
    # If the request includes the word 'send' or 'email', require review.
    lowered = request.lower()
    approval_required = ("send" in lowered) or ("email" in lowered)

    return {
        "current_step": "write_complete",
        "draft": draft,
        "approval_required": approval_required,
    }


def human_review_node(state: AgentState) -> AgentState:
    # For classroom demonstration, we auto-approve.
    # In a real capstone, this would pause for a UI or operator decision.
    draft = state.get("draft", "")
    approved_text = f"[APPROVED AFTER HUMAN REVIEW] {draft}"

    return {
        "current_step": "human_review_complete",
        "approved": True,
        "final_response": approved_text,
    }


def finalize_without_review(state: AgentState) -> AgentState:
    return {
        "current_step": "done",
        "approved": None,
        "final_response": state.get("draft", ""),
    }


def route_after_write(state: AgentState) -> str:
    return "human_review" if state.get("approval_required") else "finalize"

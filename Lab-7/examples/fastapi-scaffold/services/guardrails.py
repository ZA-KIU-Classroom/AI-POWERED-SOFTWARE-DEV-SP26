from schemas.agent_state import AgentState


def requires_human_approval(state: AgentState) -> bool:
    request = state.get("user_request", "").lower()

    risky_terms = [
        "send",
        "email",
        "submit",
        "delete",
        "book",
        "purchase",
    ]

    return any(term in request for term in risky_terms)


def build_checkpoint_message(state: AgentState) -> str:
    return (
        "Approval required before this action runs. "
        f"Current request: {state.get('user_request', '')}"
    )

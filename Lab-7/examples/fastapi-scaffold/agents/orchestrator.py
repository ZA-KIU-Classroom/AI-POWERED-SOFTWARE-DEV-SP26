import asyncio

from schemas.agent_state import AgentState
from services.retry_utils import retry_with_backoff, with_timeout
from services.guardrails import requires_human_approval, build_checkpoint_message
from services.episode_logger_extension import EpisodeEvent, append_event, now_iso


async def fake_model_call(prompt: str) -> str:
    await asyncio.sleep(0.1)
    return f"Model output for: {prompt}"


async def run_orchestrator(state: AgentState) -> AgentState:
    state["current_step"] = "research"

    async def attempt_model_call(attempt: int) -> str:
        state["retry_count"] = attempt - 1
        return await with_timeout(
            fake_model_call(state["user_request"]),
            timeout_s=state.get("timeout_ms", 8000) / 1000,
        )

    try:
        research_notes = await retry_with_backoff(attempt_model_call, max_attempts=4)
        state["research_notes"] = research_notes
        state["current_step"] = "write"

        draft = f"Draft based on research: {research_notes}"
        state["final_response"] = draft

        approval_required = requires_human_approval(state)
        state["approval_required"] = approval_required

        append_event(EpisodeEvent(
            ts=now_iso(),
            event_type="model_call",
            session_id=state["session_id"],
            model="placeholder-model",
            success=True,
            retry_count=state.get("retry_count", 0),
            timeout_ms=state.get("timeout_ms", 8000),
            latency_ms=100,
            error_type=None,
            approval_required=approval_required,
            approved=None,
            cost_usd=0.0,
            notes="research then write path",
        ))

        if approval_required:
            state["current_step"] = "human_review"
            state["approved"] = False
            state["final_response"] = build_checkpoint_message(state)

        return state

    except Exception as exc:
        state["last_error"] = str(exc)
        state["current_step"] = "failed"

        append_event(EpisodeEvent(
            ts=now_iso(),
            event_type="error",
            session_id=state["session_id"],
            model="placeholder-model",
            success=False,
            retry_count=state.get("retry_count", 0),
            timeout_ms=state.get("timeout_ms", 8000),
            latency_ms=0,
            error_type=type(exc).__name__,
            approval_required=state.get("approval_required", False),
            approved=state.get("approved"),
            cost_usd=0.0,
            notes="orchestrator failure",
        ))
        return state

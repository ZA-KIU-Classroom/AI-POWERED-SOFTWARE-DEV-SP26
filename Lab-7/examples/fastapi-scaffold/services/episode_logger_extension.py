from dataclasses import dataclass, asdict
from datetime import datetime
import json
from pathlib import Path


LOG_PATH = Path("logs/episode-log-lab7.md")


@dataclass
class EpisodeEvent:
    ts: str
    event_type: str
    session_id: str
    model: str | None
    success: bool
    retry_count: int
    timeout_ms: int
    latency_ms: int
    error_type: str | None
    approval_required: bool
    approved: bool | None
    cost_usd: float
    notes: str = ""


def append_event(event: EpisodeEvent) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(asdict(event), ensure_ascii=False)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

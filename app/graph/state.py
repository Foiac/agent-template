from typing import TypedDict, List
from app.models.trace import TraceEvent

class AgentState(TypedDict):
    input: str
    plan: dict | None
    execution: dict | None
    valid: bool | None
    history: List[str]
    trace: List[TraceEvent]

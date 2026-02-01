from pydantic import BaseModel
from typing import Any, List
from datetime import datetime

class TraceEvent(BaseModel):
    agent: str
    action: str
    input: Any | None = None
    output: Any | None = None
    timestamp: str

def now():
    return datetime.utcnow().isoformat()

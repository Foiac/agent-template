from app.models.trace import TraceEvent, now

def log_trace(state, *, agent: str, action: str, input=None, output=None):
    state["trace"].append(
        TraceEvent(
            agent=agent,
            action=action,
            input=input,
            output=output,
            timestamp=now()
        )
    )
    return state

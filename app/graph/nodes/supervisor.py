from app.services.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.trace_logger import log_trace

def supervisor_node(state):
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content=open("app/prompts/supervisor.md").read()),
        HumanMessage(content=state["input"]),
    ])

    return {
        "plan": response.content,
        "history": state["history"] + ["Supervisor criou plano"]
    }

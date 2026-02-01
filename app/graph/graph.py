from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes.supervisor import supervisor_node
from app.graph.nodes.executor import executor_node
from app.graph.nodes.validator import validator_node

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("executor", executor_node)
    graph.add_node("validator", validator_node)

    graph.set_entry_point("supervisor")

    graph.add_edge("supervisor", "executor")
    graph.add_edge("executor", "validator")

    graph.add_conditional_edges(
        "validator",
        lambda state: END if state["valid"] else "executor"
    )

    return graph.compile()

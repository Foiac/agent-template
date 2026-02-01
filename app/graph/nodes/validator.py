from app.services.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage

def validator_node(state):
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content=open("app/prompts/validator.md").read()),
        HumanMessage(content=state["execution"]),
    ])

    valid = "VALID" in response.content.upper()

    return {
        "valid": valid,
        "history": state["history"] + [f"Validator: {valid}"]
    }

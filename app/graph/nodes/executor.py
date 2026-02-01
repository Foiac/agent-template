from app.services.llm import get_llm
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
)
from app.tools.math import math_tool

def executor_node(state):
    llm = get_llm().bind_tools([math_tool])

    messages = [
        SystemMessage(content=open("app/prompts/executor.md").read()),
        HumanMessage(content=state["plan"]),
    ]

    # 1️⃣ Primeira chamada
    response = llm.invoke(messages)

    # 🔑 MUITO IMPORTANTE:
    # adiciona a mensagem do assistant que contém tool_calls
    messages.append(
        AIMessage(
            content=response.content or "",
            tool_calls=response.tool_calls
        )
    )

    # 2️⃣ Executa tools se existirem
    if response.tool_calls:
        for call in response.tool_calls:
            if call["name"] == "math_tool":
                result = math_tool.invoke(call["args"])

                messages.append(
                    ToolMessage(
                        tool_call_id=call["id"],  # 🔑 precisa bater
                        content=str(result)
                    )
                )

        # 3️⃣ Segunda chamada (agora o modelo FINALIZA)
        response = llm.invoke(messages)

    return {
        "execution": response.content,
        "history": state["history"] + ["Executor executou"]
    }

# app/agent.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 1. Verifique o streaming=True
llm = ChatOpenAI(model="gpt-4o", streaming=True, temperature=0)

async def chatbot(state: AgentState, config: RunnableConfig):
    # O segredo: passar o 'config' para o ainvoke.
    # Isso propaga os listeners de streaming do grafo para o modelo.
    response = await llm.ainvoke(state["messages"], config=config)
    return {"messages": [response]}

workflow = StateGraph(AgentState)
workflow.add_node("agent", chatbot)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

agent_executor = workflow.compile()
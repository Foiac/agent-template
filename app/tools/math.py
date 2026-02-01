from langchain_core.tools import tool

@tool
def math_tool(expression: str) -> str:
    """Resolve expressões matemáticas simples"""
    return str(eval(expression))

from fastapi import APIRouter
from app.graph.graph import build_graph
from app.schemas.request import AgentRequest


router = APIRouter()
graph = build_graph()

@router.post("/agent/run")
async def run_agent(request: AgentRequest):
    result = graph.invoke({
        "input": request.input,
        "plan": None,
        "execution": None,
        "valid": None,
        "history": [],
        "trace": []
    })
    
    return result

@router.get("/health")
async def health_check():
    return {"status": "ok"}
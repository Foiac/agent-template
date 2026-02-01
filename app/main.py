# app/main.py
import json
import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.agent import agent_executor
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS para permitir que o Notebook ou Front-end acessem a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, substitua pelo seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app/main.py
async def stream_agent_updates(user_input: str):
    inputs = {"messages": [("user", user_input)]}
    
    async for event in agent_executor.astream_events(inputs, version="v2"):
        # Se for um evento de streaming de modelo de chat
        if event["event"] == "on_chat_model_stream":
            # Extrai o conteúdo do chunk de mensagem
            chunk = event["data"].get("chunk")
            if chunk and hasattr(chunk, "content"):
                token = chunk.content
                if token:
                    yield f"data: {json.dumps({'token': token})}\n\n"
                    await asyncio.sleep(0) # Libera o loop

# No app/main.py
@app.get("/chat")
async def chat(message: str):
    return StreamingResponse(
        stream_agent_updates(message),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",  # Impede buffering em proxies (como Nginx)
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/test-raw-stream")
async def test_raw():
    async def simple_gen():
        for i in range(50):
            yield f"data: Token {i}\n\n"
            await asyncio.sleep(0.1) # 100ms entre tokens
    return StreamingResponse(simple_gen(), media_type="text/event-stream")
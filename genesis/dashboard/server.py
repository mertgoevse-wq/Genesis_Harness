import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Mount templates (assuming simple static serving for HTML if needed)
# Since we just have one HTML file, we can read it directly.
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    with open(os.path.join(TEMPLATE_DIR, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We can receive commands from UI, but mostly we push
            data = await websocket.receive_text()
            await manager.broadcast(f"Received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def push_agent_update(agent_name: str, status: str, message: str):
    """Called by genesis/memory/state.py or MetaLoop to update the UI."""
    data = json.dumps({"agent": agent_name, "status": status, "message": message})
    await manager.broadcast(data)

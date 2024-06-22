from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Optional

app = FastAPI()

@app.get('/')
def home():
    return HTMLResponse(open('index.html', 'r').read())

class ConnectionManager:
    def __init__(self) -> None:
        self.active_conniction : Optional[WebSocket] = None

    async def connect(self, websocket : WebSocket):
        await websocket.accept()
        self.active_conniction = websocket

    async def send_notification(self, msg: str):
        if self.active_conniction:
            await self.active_conniction.send_text(msg)

    def disconnect(self, websocket : WebSocket):
        if self.active_conniction == websocket:
           self.active_conniction = None


manager = ConnectionManager()

@app.get('/test')
async def test():
    await manager.send_notification('Someone view test route')


@app.websocket('/notifications')
async def notifications(websocket : WebSocket):
    await manager.connect(websocket)
    try:
        ## to keep websocket conniction work
        while True:
            data = await websocket.receive_json()
            print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
"""
WebSocket 채팅 서버
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

router = APIRouter()


class ChatManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}  # username -> ws
        self.message_history: list[dict] = []  # last 200 messages

    async def connect(self, ws: WebSocket, username: str):
        await ws.accept()
        self.connections[username] = ws
        # send history
        for msg in self.message_history[-50:]:
            await ws.send_text(json.dumps(msg))
        await self.broadcast({"type": "system", "content": f"[강호] {username} 님이 강호에 발을 들였습니다.", "style": "system"})

    async def disconnect(self, username: str):
        if username in self.connections:
            del self.connections[username]
        await self.broadcast({"type": "system", "content": f"[강호] {username} 님이 자리를 떴습니다.", "style": "system"})

    async def send_message(self, username: str, content: str):
        msg = {"type": "chat", "content": content, "sender": username, "style": "chat"}
        self.message_history.append(msg)
        if len(self.message_history) > 200:
            self.message_history = self.message_history[-200:]
        await self.broadcast(msg)

    async def broadcast(self, msg: dict):
        for username, ws in list(self.connections.items()):
            try:
                await ws.send_text(json.dumps(msg))
            except Exception:
                pass


chat_manager = ChatManager()


@router.websocket("/chat/{username}")
async def chat_ws(ws: WebSocket, username: str):
    await chat_manager.connect(ws, username)
    try:
        while True:
            data = await ws.receive_text()
            try:
                payload = json.loads(data)
                content = payload.get("content", "").strip()
                if content:
                    await chat_manager.send_message(username, content)
            except json.JSONDecodeError:
                # plain text
                if data.strip():
                    await chat_manager.send_message(username, data.strip())
    except WebSocketDisconnect:
        await chat_manager.disconnect(username)


from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str

class GameMessage(BaseModel):
    type: str  # room_desc, battle_log, chat, system, npc_dialogue
    content: str
    style: str = "normal"  # normal, battle, critical, healing, warning, romance

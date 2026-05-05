
from pydantic import BaseModel
from typing import Optional, List

class RoomResponse(BaseModel):
    id: int
    name: str
    description: str
    exits: dict
    region: str

    class Config:
        from_attributes = True

class LookResponse(BaseModel):
    room: RoomResponse
    npcs: list[str] = []
    monsters: list[str] = []
    players: list[str] = []

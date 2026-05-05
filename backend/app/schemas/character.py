
from pydantic import BaseModel, Field
from typing import Optional

class CharacterCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    origin: str  # 떠돌이 고아, 몰락세가 후예, 하급 문파 외문제자, 상단 호위무사, 관가 추방검객, 의문의 기억상실자
    physique: int = Field(default=10, ge=1, le=20)
    ki: int = Field(default=10, ge=1, le=20)
    agility: int = Field(default=10, ge=1, le=20)
    insight: int = Field(default=10, ge=1, le=20)
    charm: int = Field(default=10, ge=1, le=20)
    luck: int = Field(default=10, ge=1, le=20)

class CharacterResponse(BaseModel):
    id: int
    name: str
    origin: str
    level: int
    physique: int; ki: int; agility: int; insight: int; charm: int; luck: int
    hp: int; max_hp: int; mp: int; max_mp: int
    attack: int; defense: int; speed: int
    martial_stage: str
    current_room_id: int
    exp: int
    righteousness: int; heroism: int; greed: int; coldness: int; madness: int; affection: int

    class Config:
        from_attributes = True

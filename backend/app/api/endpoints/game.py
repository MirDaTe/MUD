"""
게임 명령어 API
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import decode_access_token
from ...models.character import Character
from ...models.room import Room
from ...models.npc import NPC
from ...models.monster import Monster
from ...schemas.game import CommandRequest, GameMessage
from ...services.game_service import execute_command

router = APIRouter(prefix="/game", tags=["game"])


def get_current_user_id(authorization: str = Header(...)) -> int:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    payload = decode_access_token(authorization[7:])
    if payload is None:
        raise HTTPException(status_code=401)
    return int(payload["sub"])


@router.post("/cmd", response_model=list[GameMessage])
def send_command(req: CommandRequest, char_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    char = db.query(Character).filter(Character.id == char_id, Character.user_id == user_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    return execute_command(db, char, req.command)


@router.get("/targets")
def get_targets(char_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """현재 방의 공격/대화 가능한 대상 목록 반환 (자동완성용)"""
    char = db.query(Character).filter(Character.id == char_id, Character.user_id == user_id).first()
    if not char:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")
    room = db.query(Room).filter(Room.id == char.current_room_id).first()
    if not room:
        return {"npcs": [], "monsters": []}

    npcs = []
    for nid in (room.npc_ids or []):
        npc = db.query(NPC).filter(NPC.id == nid).first()
        if npc:
            title_str = f" [{npc.title}]" if npc.title else ""
            occ_str = f" ({npc.occupation})" if npc.occupation else ""
            npcs.append({"name": npc.name, "title": npc.title, "occupation": npc.occupation, "display": f"{npc.name}{title_str}{occ_str}"})

    monsters = []
    for mid in (room.monster_ids or []):
        mon = db.query(Monster).filter(Monster.id == mid).first()
        if mon:
            aggro_str = " ⚠선공" if getattr(mon, "is_aggro", False) else ""
            monsters.append({"name": mon.name, "hp": mon.hp, "max_hp": mon.max_hp, "is_aggro": getattr(mon, "is_aggro", False), "display": f"{mon.name} (HP:{mon.hp}){aggro_str}"})

    return {"npcs": npcs, "monsters": monsters}

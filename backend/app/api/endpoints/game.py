"""
게임 명령어 API
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import decode_access_token
from ...models.character import Character
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

"""
캐릭터 관련 API
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import decode_access_token
from ...schemas.character import CharacterCreate, CharacterResponse
from ...services.character_service import create_character, get_characters, delete_character

router = APIRouter(prefix="/characters", tags=["characters"])


def get_current_user_id(authorization: str = Header(...)) -> int:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증이 필요합니다.")
    payload = decode_access_token(authorization[7:])
    if payload is None:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    return int(payload["sub"])


@router.post("/", response_model=CharacterResponse)
def create_char(data: CharacterCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """캐릭터 생성"""
    char = create_character(db, user_id, data)
    return char


@router.get("/", response_model=list[CharacterResponse])
def list_chars(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """내 캐릭터 목록"""
    return get_characters(db, user_id)


@router.delete("/{char_id}")
def delete_char(char_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    """캐릭터 삭제"""
    ok = delete_character(db, user_id, char_id)
    if not ok:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없거나 권한이 없습니다.")
    return {"detail": "캐릭터가 삭제되었습니다."}

"""관리자 API"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import decode_access_token
from ...services.admin_service import (
    is_admin, promote_to_admin, get_all_users, get_all_characters,
    admin_set_stat, admin_teleport, admin_give_item, admin_list_rooms
)

router = APIRouter(prefix="/admin", tags=["admin"])


def admin_required(authorization: str = Header(...)) -> tuple[int, str]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    payload = decode_access_token(authorization[7:])
    if payload is None:
        raise HTTPException(status_code=401)
    return int(payload["sub"]), payload.get("username", "")


@router.get("/check")
def check_admin(user_id: int = Depends(lambda: admin_required()[0]) if False else 0,
                db: Session = Depends(get_db),
                auth: tuple = Depends(admin_required)):
    uid, uname = auth
    ok = is_admin(db, uid)
    return {"is_admin": ok, "username": uname}


@router.post("/promote/{username}")
def promote(username: str, db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")
    ok = promote_to_admin(db, username)
    if not ok:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"status": "ok", "message": f"{username} 관리자 승급 완료"}


@router.get("/users")
def list_users(db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    return get_all_users(db)


@router.get("/characters")
def list_characters(db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    return get_all_characters(db)


@router.post("/char/{char_id}/set")
def set_stat(char_id: int, field: str, value: int, db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    err = admin_set_stat(db, char_id, field, value)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return {"status": "ok"}


@router.post("/char/{char_id}/teleport")
def teleport(char_id: int, room_id: int, db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    err = admin_teleport(db, char_id, room_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return {"status": "ok"}


@router.post("/char/{char_id}/giveitem")
def give_item(char_id: int, item_id: int, quantity: int = 1, db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    err = admin_give_item(db, char_id, item_id, quantity)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return {"status": "ok"}


@router.get("/rooms")
def list_rooms(db: Session = Depends(get_db), auth: tuple = Depends(admin_required)):
    uid, _ = auth
    if not is_admin(db, uid):
        raise HTTPException(status_code=403)
    return admin_list_rooms(db)

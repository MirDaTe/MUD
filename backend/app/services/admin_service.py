"""관리자 서비스"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.character import Character
from ..models.room import Room


def is_admin(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    return user is not None and user.is_admin


def promote_to_admin(db: Session, username: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    user.is_admin = True
    db.commit()
    return True


def get_all_users(db: Session) -> list[dict]:
    users = db.query(User).all()
    return [
        {"id": u.id, "username": u.username, "email": u.email,
         "is_admin": u.is_admin, "created_at": str(u.created_at), "last_login": str(u.last_login)}
        for u in users
    ]


def get_all_characters(db: Session) -> list[dict]:
    chars = db.query(Character).all()
    return [
        {"id": c.id, "name": c.name, "user_id": c.user_id, "level": c.level,
         "hp": c.hp, "max_hp": c.max_hp, "mp": c.mp, "max_mp": c.mp,
         "martial_stage": c.martial_stage, "current_room_id": c.current_room_id,
         "exp": c.exp, "origin": c.origin}
        for c in chars
    ]


def admin_set_stat(db: Session, char_id: int, field: str, value: int) -> Optional[str]:
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        return "캐릭터를 찾을 수 없습니다."

    valid_fields = {
        "level": "level", "exp": "exp", "hp": "hp", "max_hp": "max_hp",
        "mp": "mp", "max_mp": "max_mp", "attack": "attack", "defense": "defense",
        "speed": "speed", "physique": "physique", "ki": "ki", "agility": "agility",
        "insight": "insight", "charm": "charm", "luck": "luck",
        "righteousness": "righteousness", "heroism": "heroism",
        "greed": "greed", "coldness": "coldness", "madness": "madness",
        "affection": "affection", "martial_stage": "martial_stage"
    }

    if field not in valid_fields:
        return f"유효하지 않은 필드입니다. 사용 가능: {', '.join(valid_fields.keys())}"

    setattr(char, valid_fields[field], value)
    if field in ("max_hp", "hp"):
        char.hp = char.max_hp
    if field == "max_mp":
        char.mp = char.max_mp
    db.commit()
    return None


def admin_teleport(db: Session, char_id: int, room_id: int) -> Optional[str]:
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        return "캐릭터를 찾을 수 없습니다."
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        return "방을 찾을 수 없습니다."
    char.current_room_id = room_id
    db.commit()
    return None


def admin_give_item(db: Session, char_id: int, item_id: int, quantity: int = 1) -> Optional[str]:
    from ..models.inventory import Inventory
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        return "캐릭터를 찾을 수 없습니다."
    from ..models.item import Item as ItemModel
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        return "아이템을 찾을 수 없습니다."

    inv = db.query(Inventory).filter(
        Inventory.character_id == char_id,
        Inventory.item_id == item_id
    ).first()
    if inv:
        inv.quantity += quantity
    else:
        db.add(Inventory(character_id=char_id, item_id=item_id, quantity=quantity))
    db.commit()
    return None


def admin_list_rooms(db: Session) -> list[dict]:
    rooms = db.query(Room).order_by(Room.id).all()
    return [{"id": r.id, "name": r.name, "region": r.region, "exits": r.exits} for r in rooms]

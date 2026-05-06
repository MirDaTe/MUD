"""관리자 서비스"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.user import User
from ..models.character import Character
from ..models.room import Room
from ..models.item import Item as ItemModel
from ..models.inventory import Inventory


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
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        return "캐릭터를 찾을 수 없습니다."
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


def admin_list_rooms(
    db: Session,
    region: Optional[str] = None,
    is_safe: Optional[bool] = None,
    is_inn: Optional[bool] = None,
) -> list[dict]:
    query = db.query(Room)
    if region is not None:
        query = query.filter(Room.region == region)
    if is_safe is not None:
        query = query.filter(Room.is_safe == is_safe)
    if is_inn is not None:
        query = query.filter(Room.is_inn == is_inn)
    rooms = query.order_by(Room.id).all()
    return [{"id": r.id, "name": r.name, "region": r.region, "is_safe": r.is_safe, "is_inn": r.is_inn, "exits": r.exits} for r in rooms]


def admin_list_items(
    db: Session,
    search: Optional[str] = None,
    item_type: Optional[str] = None,
) -> list[dict]:
    """아이템 검색/목록. search가 있으면 name/code/sub_type으로 LIKE 검색. 최대 50개 반환."""
    query = db.query(ItemModel)
    if item_type is not None:
        query = query.filter(ItemModel.item_type == item_type)
    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            ItemModel.name.ilike(like_pattern)
            | ItemModel.code.ilike(like_pattern)
            | ItemModel.sub_type.ilike(like_pattern)
        )
    items = query.limit(50).all()
    return [
        {
            "id": item.id,
            "code": item.code,
            "name": item.name,
            "item_type": item.item_type,
            "sub_type": item.sub_type,
            "rarity": item.rarity,
            "price": item.price,
            "description": item.description,
        }
        for item in items
    ]


def admin_get_item(db: Session, item_id: int) -> Optional[dict]:
    """아이템 상세 정보."""
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        return None
    return {
        "id": item.id,
        "code": item.code,
        "name": item.name,
        "item_type": item.item_type,
        "sub_type": item.sub_type,
        "slot": item.slot,
        "weapon_type": item.weapon_type,
        "description": item.description,
        "stats": item.stats,
        "effects": item.effects,
        "price": item.price,
        "rarity": item.rarity,
        "stack_limit": item.stack_limit,
    }


def admin_give_item_by_code(
    db: Session,
    char_id: int,
    item_code: str,
    quantity: int = 1,
) -> Optional[str]:
    """코드로 아이템 지급."""
    char = db.query(Character).filter(Character.id == char_id).first()
    if not char:
        return "캐릭터를 찾을 수 없습니다."

    item = db.query(ItemModel).filter(ItemModel.code == item_code).first()
    if not item:
        return f"아이템 코드 '{item_code}'를 찾을 수 없습니다."

    inv = db.query(Inventory).filter(
        Inventory.character_id == char_id,
        Inventory.item_id == item.id,
    ).first()
    if inv:
        inv.quantity += quantity
    else:
        db.add(Inventory(character_id=char_id, item_id=item.id, quantity=quantity))
    db.commit()
    return None

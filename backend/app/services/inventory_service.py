"""인벤토리 서비스 — 판매, 분해, 버리기, 장비현황"""
from typing import Optional
from sqlalchemy.orm import Session
from ..models.character import Character
from ..models.inventory import Inventory
from ..models.item import Item


def sell_item(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """아이템 판매 (반값에 매각)"""
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0  # 장착중이 아닌 것만
    ).first()
    if not inv:
        return "판매 가능한 해당 아이템이 없습니다 (장착중이면 해제 후 판매하세요)."
    if inv.quantity < quantity:
        return f"수량이 부족합니다. (보유: {inv.quantity})"

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    sell_price = (item.price or 10) // 2  # 반값

    inv.quantity -= quantity
    if inv.quantity <= 0:
        db.delete(inv)

    char.gold += sell_price * quantity
    db.commit()
    return None


def dismantle_item(db: Session, char: Character, item_name: str) -> Optional[str]:
    """아이템 분해 (강화석 획득 확률)"""
    import random
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0
    ).first()
    if not inv:
        return "분해 가능한 해당 아이템이 없습니다."

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    rarity = item.rarity or 1

    # 분해 보상: 강화석 (ID 151)
    stone_count = random.randint(rarity, rarity * 2)
    stone = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.item_id == 151
    ).first()
    if stone:
        stone.quantity += stone_count
    else:
        db.add(Inventory(character_id=char.id, item_id=151, quantity=stone_count))

    inv.quantity -= 1
    if inv.quantity <= 0:
        db.delete(inv)
    db.commit()
    return None


def discard_item(db: Session, char: Character, item_name: str, quantity: int = 1) -> Optional[str]:
    """아이템 버리기"""
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 0
    ).first()
    if not inv:
        return "버릴 수 있는 해당 아이템이 없습니다."
    if inv.quantity < quantity:
        return f"수량이 부족합니다. (보유: {inv.quantity})"

    inv.quantity -= quantity
    if inv.quantity <= 0:
        db.delete(inv)
    db.commit()
    return None


def equip_status(db: Session, char: Character) -> dict:
    """장비 장착 현황"""
    equipped = db.query(Inventory).filter(
        Inventory.character_id == char.id,
        Inventory.equipped == 1
    ).all()

    slots = {"weapon": None, "armor": None, "accessory": None}
    for inv in equipped:
        item = db.query(Item).filter(Item.id == inv.item_id).first()
        if item and item.item_type in slots:
            slots[item.item_type] = {"name": item.name, "stats": item.stats, "enchant": inv.id}

    return {"slots": slots, "total_attack": char.attack, "total_defense": char.defense,
            "max_hp": char.max_hp, "max_mp": char.max_mp, "speed": char.speed, "crit_rate": char.crit_rate}


def unequip(db: Session, char: Character, item_name: str) -> Optional[str]:
    """장비 해제"""
    inv = db.query(Inventory).join(Item).filter(
        Inventory.character_id == char.id,
        Item.name.ilike(f"%{item_name}%"),
        Inventory.equipped == 1
    ).first()
    if not inv:
        return "장착 중인 해당 아이템이 없습니다."

    item = db.query(Item).filter(Item.id == inv.item_id).first()
    stats = item.stats or {}
    char.attack -= stats.get("attack", 0)
    char.defense -= stats.get("defense", 0)
    char.max_hp -= stats.get("hp", 0)
    char.max_mp -= stats.get("mp", 0)
    char.speed -= stats.get("speed", 0)
    char.hp = min(char.hp, char.max_hp)
    char.mp = min(char.mp, char.max_mp)

    inv.equipped = 0
    db.commit()
    return None
